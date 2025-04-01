import locale
from byzerllm.utils import format_str_jinja2

MESSAGES = {
    "en": {
        "models_no_active": "No active models found",
        "models_speed_test_results": "Model Speed Test Results",
        "models_testing": "Testing model: {{name}}...",
        "models_testing_start": "Starting speed test for all active models...",
        "models_testing_progress": "Testing progress: {{ completed }}/{{ total }} models",
        "generation_cancelled": "[Interrupted] Generation cancelled",
        "model_not_found": "Model {{model_name}} not found",
        "generating_shell_script": "Generating Shell Script",
        "new_session_started": "New session started. Previous chat history has been archived.",    
        "memory_save_success": "✅ Saved to your memory",
        "file_decode_error": "Failed to decode file: {{file_path}}. Tried encodings: {{encodings}}",
        "file_write_error": "Failed to write file: {{file_path}}. Error: {{error}}",
        "yaml_load_error": "Error loading yaml file {{yaml_file}}: {{error}}",
        "git_command_error": "Git command execution error: {{error}}",
        "get_commit_diff_error": "Error getting commit diff: {{error}}",
        "no_latest_commit": "Unable to get latest commit information",
        "code_review_error": "Code review process error: {{error}}",
        "index_file_too_large": "⚠️ File {{ file_path }} is too large ({{ file_size }} > {{ max_length }}), splitting into chunks...",
        "index_update_success": "✅ {{ model_name }} Successfully updated index for {{ file_path }} (md5: {{ md5 }}) in {{ duration }}s",
        "index_build_error": "❌ {{ model_name }} Error building index for {{ file_path }}: {{ error }}",
        "index_build_summary": "📊 Total Files: {{ total_files }}, Need to Build Index: {{ num_files }}",
        "building_index_progress": "⏳ Building Index: {{ counter }}/{{ num_files }}...",
        "index_source_dir_mismatch": "⚠️ Source directory mismatch (file_path: {{ file_path }}, source_dir: {{ source_dir }})",
        "index_related_files_fail": "⚠️ Failed to find related files for chunk {{ chunk_count }}",
        "index_threads_completed": "✅ Completed {{ completed_threads }}/{{ total_threads }} threads",
        "index_related_files_fail": "⚠️ Failed to find related files for chunk {{ chunk_count }}",
        "index_file_removed": "🗑️ Removed non-existent file index: {{ file_path }}",
        "index_file_saved": "💾 Saved index file, updated {{ updated_files }} files, removed {{ removed_files }} files",
        "human_as_model_instructions": (
            "You are now in Human as Model mode. The content has been copied to your clipboard.\n"
            "The system is waiting for your input. When finished, enter 'EOF' on a new line to submit.\n"
            "Use '/break' to exit this mode. If you have issues with copy-paste, use '/clear' to clean and paste again."
        ),
        "clipboard_not_supported": (
            "pyperclip not installed or clipboard is not supported, instruction will not be copied to clipboard."
        ),
        "human_as_model_instructions_no_clipboard": (
            "You are now in Human as Model mode. [bold red]The content could not be copied to your clipboard.[/bold red]\n"
            "but you can copy prompt from output.txt file.\n"
            "The system is waiting for your input. When finished, enter 'EOF' on a new line to submit.\n"
            "Use '/break' to exit this mode. If you have issues with copy-paste, use '/clear' to clean and paste again."
        ),
        "phase1_processing_sources": "Phase 1: Processing REST/RAG/Search sources...",
        "phase2_building_index": "Phase 2: Building index for all files...",
        "phase6_file_selection": "Phase 6: Processing file selection and limits...",
        "phase7_preparing_output": "Phase 7: Preparing final output...",
        "chat_human_as_model_instructions": (
            "Chat is now in Human as Model mode.\n"
            "The question has been copied to your clipboard.\n"
            "Please use Web version model to get the answer.\n"
            "Or use /conf human_as_model:false to close this mode and get the answer in terminal directly."
            "Paste the answer to the input box below, use '/break' to exit, '/clear' to clear the screen, '/eof' to submit."
        ),
        "code_generation_start": "Auto generate the code...",
        "code_generation_complete": "Code generation completed in {{ duration }} seconds, input_tokens_count: {{ input_tokens }}, generated_tokens_count: {{ output_tokens }}, speed: {{ speed }} tokens/s",
        "code_merge_start": "Auto merge the code...",
        "code_execution_warning": "Content(send to model) is {{ content_length }} tokens (you may collect too much files), which is larger than the maximum input length {{ max_length }}",
        "quick_filter_start": "{{ model_name }} Starting filter context(quick_filter)...",
        "normal_filter_start": "{{ model_name }} Starting filter context(normal_filter)...",
        "pylint_check_failed": "⚠️ Pylint check failed: {{ error_message }}",
        "pylint_error": "❌ Error running pylint: {{ error_message }}",
        "unmerged_blocks_warning": "⚠️ Found {{ num_blocks }} unmerged blocks, the changes will not be applied. Please review them manually then try again.",
        "pylint_file_check_failed": "⚠️ Pylint check failed for {{ file_path }}. Changes not applied. Error: {{ error_message }}",
        "merge_success": "✅ Merged changes in {{ num_files }} files {{ num_changes }}/{{ total_blocks }} blocks.",
        "no_changes_made": "⚠️ No changes were made to any files.",
        "files_merged": "✅ Merged {{ total }} files into the project.",
        "merge_failed": "❌ Merge file {{ path }} failed: {{ error }}",
        "files_merged_total": "✅ Merged {{ total }} files into the project.",
        "ranking_skip": "Only 1 candidate, skip ranking",
        "ranking_start": "Start ranking {{ count }} candidates using model {{ model_name }}",
        "ranking_failed_request": "Ranking request failed: {{ error }}",
        "ranking_all_failed": "All ranking requests failed",
        "ranking_complete": "Ranking completed in {{ elapsed }}s, total voters: {{ total_tasks }}, best candidate index: {{ best_candidate }}, scores: {{ scores }}, input_tokens: {{ input_tokens }}, output_tokens: {{ output_tokens }}",
        "ranking_process_failed": "Ranking process failed: {{ error }}",
        "ranking_failed": "Ranking failed in {{ elapsed }}s, using original order",
        "begin_index_source_code": "🚀 Begin to index source code in {{ source_dir }}",
        "stream_out_stats": "Elapsed time {{ elapsed_time }} seconds, first token time: {{ first_token_time }} seconds, input tokens: {{ input_tokens }}, output tokens: {{ output_tokens }}, speed: {{ speed }} tokens/s",
        "quick_filter_stats": "快速过滤器完成，耗时 {{ elapsed_time }} 秒，输入token数: {{ input_tokens }}, 输出token数: {{ output_tokens }}",
        "upsert_file": "✅ Updated file: {{ file_path }}",  
        "unmerged_blocks_title": "Unmerged Blocks",
        "quick_filter_title": "{{ model_name }} is analyzing how to filter context...",
        "quick_filter_failed": "❌ Quick filter failed: {{ error }}. ",
        "unmerged_file_path": "File: {{file_path}}",
        "unmerged_search_block": "Search Block({{similarity}}):",
        "unmerged_replace_block": "Replace Block:",
        "unmerged_blocks_total": "Total unmerged blocks: {{num_blocks}}",
        "git_init_required": "⚠️ auto_merge only applies to git repositories.\n\nPlease try using git init in the source directory:\n\n```shell\ncd {{ source_dir }}\ngit init.\n```\n\nThen run auto - coder again.\nError: {{ error }}",
        "quick_filter_reason": "Auto get(quick_filter mode)",
        "quick_filter_too_long": "⚠️ index file is too large ({{ tokens_len }}/{{ max_tokens }}). The query will be split into {{ split_size }} chunks.",
        "quick_filter_tokens_len": "📊 Current index size: {{ tokens_len }} tokens",
        "estimated_chat_input_tokens": "Estimated chat input tokens: {{ estimated_input_tokens }}",
        "estimated_input_tokens_in_generate": "Estimated input tokens in generate ({{ generate_mode }}): {{ estimated_input_tokens }}",
    },
    "zh": {
        "models_no_active": "未找到激活的模型",
        "models_speed_test_results": "模型速度测试结果",
        "models_testing": "正在测试模型: {{name}}...",
        "models_testing_start": "开始对所有激活的模型进行速度测试...",
        "generation_cancelled": "[已中断] 生成已取消",
        "model_not_found": "未找到模型: {{model_name}}",
        "generating_shell_script": "正在生成 Shell 脚本",
        "new_session_started": "新会话已开始。之前的聊天历史已存档。",
        "memory_save_success": "✅ 已保存到您的记忆中",
        "file_decode_error": "无法解码文件: {{file_path}}。尝试的编码: {{encodings}}",
        "file_write_error": "无法写入文件: {{file_path}}. 错误: {{error}}",
        "yaml_load_error": "加载YAML文件出错 {{yaml_file}}: {{error}}",
        "git_command_error": "Git命令执行错误: {{error}}",
        "get_commit_diff_error": "获取commit diff时出错: {{error}}",
        "no_latest_commit": "无法获取最新的提交信息",
        "code_review_error": "代码审查过程出错: {{error}}",
        "index_file_too_large": "⚠️ 文件 {{ file_path }} 过大 ({{ file_size }} > {{ max_length }}), 正在分块处理...",
        "index_update_success": "✅ {{ model_name }} 成功更新 {{ file_path }} 的索引 (md5: {{ md5 }}), 耗时 {{ duration }} 秒",
        "index_build_error": "❌ {{ model_name }} 构建 {{ file_path }} 索引时出错: {{ error }}",
        "index_build_summary": "📊 总文件数: {{ total_files }}, 需要构建索引: {{ num_files }}",
        "building_index_progress": "⏳ 正在构建索引: {{ counter }}/{{ num_files }}...",
        "index_source_dir_mismatch": "⚠️ 源目录不匹配 (文件路径: {{ file_path }}, 源目录: {{ source_dir }})",
        "index_related_files_fail": "⚠️ 无法为块 {{ chunk_count }} 找到相关文件",
        "index_threads_completed": "✅ 已完成 {{ completed_threads }}/{{ total_threads }} 个线程",
        "index_related_files_fail": "⚠️ 无法为块 {{ chunk_count }} 找到相关文件",
        "index_file_removed": "🗑️ 已移除不存在的文件索引：{{ file_path }}",
        "index_file_saved": "💾 已保存索引文件，更新了 {{ updated_files }} 个文件，移除了 {{ removed_files }} 个文件",
        "human_as_model_instructions": (
            "您现在处于人类作为模型模式。内容已复制到您的剪贴板。\n"
            "系统正在等待您的输入。完成后，在新行输入'EOF'提交。\n"
            "使用'/break'退出此模式。如果复制粘贴有问题，使用'/clear'清理并重新粘贴。"
        ),
        "clipboard_not_supported": (
            "未安装pyperclip或不支持剪贴板，指令将不会被复制到剪贴板。"
        ),
        "human_as_model_instructions_no_clipboard": (
            "您现在处于人类作为模型模式。[bold red]内容无法复制到您的剪贴板。[/bold red]\n"
            "但您可以从output.txt文件复制提示。\n"
            "系统正在等待您的输入。完成后，在新行输入'EOF'提交。\n"
            "使用'/break'退出此模式。如果复制粘贴有问题，使用'/clear'清理并重新粘贴。"
        ),
        "phase1_processing_sources": "阶段 1: 正在处理 REST/RAG/Search 源...",
        "phase2_building_index": "阶段 2: 正在为所有文件构建索引...",
        "phase6_file_selection": "阶段 6: 正在处理文件选择和限制...",
        "phase7_preparing_output": "阶段 7: 正在准备最终输出...",
        "chat_human_as_model_instructions": (
            "\n============= Chat 处于 Human as Model 模式 =============\n"
            "问题已复制到剪贴板\n"
            "请使用Web版本模型获取答案\n"
            "或者使用 /conf human_as_model:false 关闭该模式直接在终端获得答案。"
            "将获得答案黏贴到下面的输入框，换行后，使用 '/break' 退出，'/clear' 清屏，'/eof' 提交。"
        ),
        "code_generation_start": "正在自动生成代码...",
        "code_generation_complete": "代码生成完成，耗时 {{ duration }} 秒，输入token数: {{ input_tokens }}, 输出token数: {{ output_tokens }}, 速度: {{ speed }} tokens/秒",
        "code_merge_start": "正在自动合并代码...",
        "code_execution_warning": "发送给模型的内容长度为 {{ content_length }} tokens（您可能收集了太多文件），超过了最大输入长度 {{ max_length }}",
        "quick_filter_start": "{{ model_name }} 开始查找上下文(quick_filter)...",
        "normal_filter_start": "{{ model_name }} 开始查找上下文(normal_filter)...",
        "pylint_check_failed": "⚠️ Pylint 检查失败: {{ error_message }}",
        "pylint_error": "❌ 运行 Pylint 时出错: {{ error_message }}",
        "begin_index_source_code": "🚀 开始为 {{ source_dir }} 中的源代码建立索引",
        "unmerged_blocks_warning": "⚠️ 发现 {{ num_blocks }} 个未合并的代码块，更改将不会被应用。请手动检查后重试。",
        "pylint_file_check_failed": "⚠️ {{ file_path }} 的 Pylint 检查失败。更改未应用。错误: {{ error_message }}",
        "merge_success": "✅ 成功合并了 {{ num_files }} 个文件中的更改 {{ num_changes }}/{{ total_blocks }} 个代码块。",
        "no_changes_made": "⚠️ 未对任何文件进行更改。",
        "unmerged_blocks_title": "未合并代码块",
        "unmerged_file_path": "文件: {{file_path}}",
        "unmerged_search_block": "Search Block({{similarity}}):",
        "unmerged_replace_block": "Replace Block:",
        "unmerged_blocks_total": "未合并代码块数量: {{num_blocks}}",
        "git_init_required": "⚠️ auto_merge 仅适用于 git 仓库。\n\n请尝试在源目录中使用 git init:\n\n```shell\ncd {{ source_dir }}\ngit init.\n```\n\n然后再次运行 auto-coder。\n错误: {{ error }}",
        "quick_filter_reason": "自动获取(quick_filter模式)",
        "quick_filter_too_long": "⚠️ 索引文件过大 ({{ tokens_len }}/{{ max_tokens }})。查询将被分成 {{ split_size }} 个部分执行。",
        "quick_filter_tokens_len": "📊 当前索引大小: {{ tokens_len }} tokens",
        "upsert_file": "✅ 更新文件: {{ file_path }}",
        "files_merged": "✅ 成功合并了 {{ total }} 个文件到项目中。",
        "merge_failed": "❌ 合并文件 {{ path }} 失败: {{ error }}",
        "files_merged_total": "✅ 合并了 {{ total }} 个文件到项目中。",
        "ranking_skip": "只有1个候选项，跳过排序",
        "ranking_start": "开始对 {{ count }} 个候选项进行排序,使用模型 {{ model_name }} 打分",
        "ranking_failed_request": "排序请求失败: {{ error }}",
        "ranking_all_failed": "所有排序请求都失败",
        "ranking_complete": "排序完成，耗时 {{ elapsed }} 秒，总投票数: {{ total_tasks }}，最佳候选索引: {{ best_candidate }}，得分: {{ scores }}，输入token数: {{ input_tokens }}，输出token数: {{ output_tokens }}",
        "ranking_process_failed": "排序过程失败: {{ error }}",
        "ranking_failed": "排序失败，耗时 {{ elapsed }} 秒，使用原始顺序",
        "stream_out_stats": "总耗时 {{ elapsed_time }} 秒，首token时间: {{ first_token_time }} 秒，输入token数: {{ input_tokens }}, 输出token数: {{ output_tokens }}, 速度: {{ speed }} tokens/秒",
        "quick_filter_stats": "Quick filter completed in {{ elapsed_time }} seconds, input tokens: {{ input_tokens }}, output tokens: {{ output_tokens }}",
        "quick_filter_title": "{{ model_name }} 正在分析如何筛选上下文...",
        "quick_filter_failed": "❌ 快速过滤器失败: {{ error }}. ",
        "estimated_chat_input_tokens": "对话输入token预估为: {{ estimated_input_tokens }}",
        "estimated_input_tokens_in_generate": "生成代码({{ generate_mode }})预计输入token数: {{ estimated_input_tokens_in_generate }}",
    },
}


def get_system_language():
    try:
        return locale.getdefaultlocale()[0][:2]
    except:
        return 'en'


def get_message(key):
    lang = get_system_language()
    return MESSAGES.get(lang, MESSAGES['en']).get(key, MESSAGES['en'][key])

def get_message_with_format(msg_key: str, **kwargs):
    return format_str_jinja2(get_message(msg_key), **kwargs)
