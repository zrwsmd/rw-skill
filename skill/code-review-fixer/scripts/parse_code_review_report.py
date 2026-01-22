#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从代码审查报告 HTML 中提取指定严重程度的问题列表
支持格式：代码审查报告_赵瑞文_*.html 或 Dai-Ma-Shen-Cha-Bao-Gao-*.html
"""

import argparse
import json
import re
from pathlib import Path
from typing import List, Dict, Optional

def extract_issues_from_html(html_path: Path, target_severity: Optional[str] = None) -> List[Dict]:
    """
    从HTML中提取问题列表
    
    Args:
        html_path: HTML文件路径
        target_severity: 目标严重程度（严重/中等/轻微/误报），None表示全部
    
    Returns:
        问题列表（字典列表）
    """
    html = html_path.read_text(encoding='utf-8', errors='ignore')
    
    # 正则提取 h5 标签中的问题标题（格式：🔴 严重: 问题描述）
    h5_pattern = re.compile(
        r'<h5[^>]*>\s*(?:🔴|🟡|🟢|⚪)?\s*(严重|中等|轻微|误报)\s*[:：]\s*(.+?)\s*</h5>',
        re.S | re.I
    )
    
    raw_issues = []
    for match in h5_pattern.finditer(html):
        severity = match.group(1).strip()
        title = match.group(2).strip()
        # 清理HTML标签和多余空格
        title = re.sub(r'<[^>]+>', '', title)
        title = re.sub(r'\s+', ' ', title).strip()
        
        # 记录匹配位置，用于后续提取上下文
        start_pos = match.start()
        end_pos = match.end()
        
        raw_issues.append({
            "severity": severity,
            "title": title,
            "start_pos": start_pos,
            "end_pos": end_pos
        })
    
    # 筛选目标严重程度
    if target_severity:
        raw_issues = [issue for issue in raw_issues if issue['severity'] == target_severity]
    
    # 提取每个问题的详细信息
    enriched_issues = []
    for idx, issue in enumerate(raw_issues, start=1):
        # 提取问题上下文（h5 标签后的内容，直到下一个 h5 或结尾）
        start = issue['end_pos']
        # 找到下一个问题的位置
        next_issue_pos = len(html)
        if idx < len(raw_issues):
            next_issue_pos = raw_issues[idx]['start_pos'] if idx < len(raw_issues) else len(html)
        
        context = html[start:next_issue_pos]
        
        # 提取文件路径和行号
        file_info = extract_file_info(context, html, issue['start_pos'])
        
        # 提取问题描述
        description = extract_description(context)
        
        # 提取改进建议
        suggestion = extract_suggestion(context)
        
        # 提取代码示例
        code_example = extract_code_example(context)
        
        enriched_issues.append({
            "id": idx,
            "severity": issue['severity'],
            "title": issue['title'],
            "file": file_info.get('file', '未知文件'),
            "line": file_info.get('line'),
            "description": description or issue['title'],
            "suggestion": suggestion or "请参考报告中的改进建议",
            "code_example": code_example
        })
    
    return enriched_issues


def extract_file_info(context: str, full_html: str, problem_pos: int) -> Dict[str, Optional[str]]:
    """
    提取文件路径和行号信息
    优先从上下文中查找，如果没有则在问题位置前查找
    """
    # 模式1: "涉及文件与行号: src/language/test28.js:4-6"
    pattern1 = re.search(r'涉及文件与行号[：:]\s*([\w/.-]+\.\w+)\s*[:：]?\s*(\d+-?\d*)?', context)
    if pattern1:
        return {"file": pattern1.group(1), "line": pattern1.group(2)}
    
    # 模式2: 直接的文件路径格式 "src/language/test28.js"
    file_pattern = re.compile(r'((?:src/|[\w-]+/)?[\w/-]+\.(js|ts|html|md|py|css|jsx|tsx|vue))')
    
    # 先在上下文中查找
    context_matches = file_pattern.findall(context)
    if context_matches:
        return {"file": context_matches[0][0], "line": None}
    
    # 在问题前500字符内查找
    before_context = full_html[max(0, problem_pos - 500):problem_pos]
    before_matches = file_pattern.findall(before_context)
    if before_matches:
        # 取最后一个匹配（最接近问题的）
        return {"file": before_matches[-1][0], "line": None}
    
    return {"file": "未知文件", "line": None}


def extract_description(context: str) -> Optional[str]:
    """
    提取问题描述部分
    通常在 "**问题描述**:" 或 "问题描述：" 之后
    """
    # 模式1: Markdown 加粗格式
    pattern1 = re.search(r'\*\*问题描述\*\*\s*[：:]\s*(.+?)(?:\*\*|$)', context, re.S)
    if pattern1:
        desc = pattern1.group(1).strip()
        # 清理HTML标签
        desc = re.sub(r'<[^>]+>', '', desc)
        # 截取前300字符（避免过长）
        return desc[:300] + ('...' if len(desc) > 300 else '')
    
    # 模式2: 纯文本格式
    pattern2 = re.search(r'问题描述\s*[：:]\s*(.+?)(?:\n\n|风险|原因|改进|$)', context, re.S)
    if pattern2:
        desc = pattern2.group(1).strip()
        desc = re.sub(r'<[^>]+>', '', desc)
        return desc[:300] + ('...' if len(desc) > 300 else '')
    
    return None


def extract_suggestion(context: str) -> Optional[str]:
    """
    提取改进建议部分
    """
    # 模式1: Markdown 加粗格式
    pattern1 = re.search(r'\*\*改进建议\*\*\s*[：:]\s*(.+?)(?:\*\*|优化代码示例|$)', context, re.S)
    if pattern1:
        suggestion = pattern1.group(1).strip()
        suggestion = re.sub(r'<[^>]+>', '', suggestion)
        return suggestion[:500] + ('...' if len(suggestion) > 500 else '')
    
    # 模式2: 纯文本格式
    pattern2 = re.search(r'改进建议\s*[：:]\s*(.+?)(?:\n\n|优化代码|示例|$)', context, re.S)
    if pattern2:
        suggestion = pattern2.group(1).strip()
        suggestion = re.sub(r'<[^>]+>', '', suggestion)
        return suggestion[:500] + ('...' if len(suggestion) > 500 else '')
    
    return None


def extract_code_example(context: str) -> Optional[str]:
    """
    提取优化代码示例
    通常在代码块中：```language ... ```
    """
    # 提取 Markdown 代码块
    code_pattern = re.compile(r'```[\w]*\s*\n(.+?)\n```', re.S)
    matches = code_pattern.findall(context)
    
    if matches:
        # 返回第一个代码块（通常是优化后的代码）
        code = matches[0].strip()
        return code
    
    # 尝试提取 HTML <pre> 或 <code> 标签
    html_code_pattern = re.compile(r'<(?:pre|code)[^>]*>(.+?)</(?:pre|code)>', re.S)
    html_matches = html_code_pattern.findall(context)
    if html_matches:
        code = html_matches[0].strip()
        code = re.sub(r'<[^>]+>', '', code)  # 清理内部HTML标签
        return code
    
    return None


def main():
    parser = argparse.ArgumentParser(
        description='从代码审查报告HTML中提取问题列表',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例用法:
  # 提取所有严重问题
  python parse_code_review_report.py --input report.html --severity 严重

  # 提取所有问题
  python parse_code_review_report.py --input report.html

  # 指定输出位置
  python parse_code_review_report.py --input report.html --severity 中等 --output ./issues.json
        '''
    )
    parser.add_argument('--input', required=True, help='输入HTML报告路径')
    parser.add_argument('--severity', choices=['严重', '中等', '轻微', '误报'], help='筛选严重程度')
    parser.add_argument('--output', default='/tmp/issues.json', help='输出JSON路径（默认: /tmp/issues.json）')
    parser.add_argument('--verbose', action='store_true', help='显示详细输出')
    args = parser.parse_args()
    
    html_path = Path(args.input)
    if not html_path.exists():
        print(f"❌ 错误：文件不存在 {html_path}")
        return 1
    
    try:
        issues = extract_issues_from_html(html_path, args.severity)
        
        if args.verbose:
            print(f"\n📋 提取到 {len(issues)} 个问题（严重程度：{args.severity or '全部'}）\n")
            for issue in issues:
                print(f"  [{issue['id']}] {issue['severity']} - {issue['title']}")
                print(f"      文件: {issue['file']}" + (f" (行 {issue['line']})" if issue['line'] else ""))
                print()
        
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(issues, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        
        print(f"✅ 成功提取 {len(issues)} 个问题")
        print(f"📁 输出到: {output_path.absolute()}")
        
        return 0
    
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
