import byzerllm
from typing import List, Union
from autocoder.common import AutoCoderArgs
from autocoder.common.types import CodeGenerateResult
from pydantic import BaseModel
from autocoder.common.printer import Printer
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback
from autocoder.common.utils_code_auto_generate import chat_with_continue
from byzerllm.utils.str2model import to_model

from autocoder.utils.llms import get_llm_names
class RankResult(BaseModel):
    rank_result: List[int]


class CodeModificationRanker:
    def __init__(self, llm: byzerllm.ByzerLLM, args: AutoCoderArgs):
        self.llm = llm
        self.args = args
        self.llms = self.llm.get_sub_client(
            "generate_rerank_model") or [self.llm]
        if not isinstance(self.llms, list):
            self.llms = [self.llms]
        self.printer = Printer()

    @byzerllm.prompt()
    def _rank_modifications(self, s: CodeGenerateResult) -> str:
        '''
        对一组代码修改进行质量评估并排序。

        下面是修改需求：

        <edit_requirement>
        {{ s.conversations[0][-2]["content"] }}
        </edit_requirement>

        下面是相应的代码修改：
        {% for content in s.contents %}
        <edit_block id="{{ loop.index0 }}">
        {{content}}
        </edit_block>
        {% endfor %}

        请输出如下格式的评估结果,只包含 JSON 数据:

        ```json
        {
            "rank_result": [id1, id2, id3] 
        }
        ```

        注意：   
        1. id 为 edit_block 的 id,按质量从高到低排序，并且 id 必须是数字        
        2. 只输出前面要求的 Json 格式就好，不要输出其他内容，Json 需要使用 ```json ```包裹                
        '''

    def rank_modifications(self, generate_result: CodeGenerateResult) -> CodeGenerateResult:
        import time
        from collections import defaultdict

        start_time = time.time()

        # 如果只有一个候选，直接返回
        if len(generate_result.contents) == 1:
            self.printer.print_in_terminal("ranking_skip", style="blue")
            return generate_result

        self.printer.print_in_terminal(
            "ranking_start", style="blue", count=len(generate_result.contents))
        rank_times = self.args.rank_times_same_model
        total_tasks = len(self.llms) * rank_times

        query = self._rank_modifications.prompt(generate_result)
        input_tokens_count = 0
        generated_tokens_count = 0
        try:
            # Create a thread pool with (number of models * generate_times) workers
            with ThreadPoolExecutor(max_workers=total_tasks) as executor:
                # Submit tasks for each model and generate_times
                futures = []
                for llm in self.llms:                    
                    model_name = ",".join(get_llm_names(llm))
                    self.printer.print_in_terminal(
                        "ranking_start", style="blue", count=len(generate_result.contents), model_name=model_name)
                    
                    for _ in range(rank_times):
                        
                        futures.append(
                            executor.submit(
                                chat_with_continue,
                                llm,
                                [{"role": "user", "content": query}],
                                {}
                            )
                        )

                # Collect all results
                results = []
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        input_tokens_count += result.input_tokens_count
                        generated_tokens_count += result.generated_tokens_count
                        v = to_model(result.content,RankResult)                        
                        results.append(v.rank_result)
                    except Exception as e:
                        self.printer.print_in_terminal(
                            "ranking_failed_request", style="yellow", error=str(e))                        
                        continue

                if not results:
                    raise Exception(
                        self.printer.get_message_from_key("ranking_all_failed"))

                # Calculate scores for each candidate
                candidate_scores = defaultdict(float)
                for rank_result in results:
                    for idx, candidate_id in enumerate(rank_result):
                        # Score is 1/(position + 1) since position starts from 0
                        candidate_scores[candidate_id] += 1.0 / (idx + 1)

                # Sort candidates by score in descending order
                sorted_candidates = sorted(candidate_scores.keys(),
                                           key=lambda x: candidate_scores[x],
                                           reverse=True)

                elapsed = time.time() - start_time
                # Format scores for logging
                score_details = ", ".join(
                    [f"candidate {i}: {candidate_scores[i]:.2f}" for i in sorted_candidates])
                self.printer.print_in_terminal(
                    "ranking_complete",
                    style="green",
                    elapsed=f"{elapsed:.2f}",
                    total_tasks=total_tasks,
                    best_candidate=sorted_candidates[0],
                    scores=score_details,
                    input_tokens=input_tokens_count,
                    output_tokens=generated_tokens_count
                )

                rerank_contents = [generate_result.contents[i]
                                   for i in sorted_candidates]
                rerank_conversations = [
                    generate_result.conversations[i] for i in sorted_candidates]
                return CodeGenerateResult(contents=rerank_contents, conversations=rerank_conversations)

        except Exception as e:
            self.printer.print_in_terminal(
                "ranking_process_failed", style="red", error=str(e))            
            elapsed = time.time() - start_time
            self.printer.print_in_terminal(
                "ranking_failed", style="yellow", elapsed=f"{elapsed:.2f}")
            return generate_result
