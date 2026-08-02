#!/usr/bin/env python3
"""
HTML Generator for Mini-GTA Documentation
Converts Markdown files to beautiful HTML pages
"""

import os
import re
from pathlib import Path
from datetime import datetime

class HTMLGenerator:
    """Generate HTML files from Markdown documentation"""
    
    # Markdown files to convert
    MARKDOWN_FILES = [
        'APK_QUICKSTART.md',
        'CLOCK_README.md',
        'DEPLOYMENT_CHECKLIST.md',
        'DEPLOYMENT_SUMMARY.md',
        'ENHANCEMENT_PLAN.md',
        'FINAL_STATUS.md',
        'HOW_TO_PLAY.md',
        'HOW_TO_PLAY_GUIDE.md',
        'README.md'
    ]
    
    # CSS Styling
    CSS_STYLE = """
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        header .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        nav {
            background: #f8f9fa;
            padding: 15px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        
        nav ul {
            list-style: none;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 20px;
            padding: 0 20px;
        }
        
        nav a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        nav a:hover {
            color: #764ba2;
        }
        
        main {
            padding: 40px;
        }
        
        h1, h2, h3, h4, h5, h6 {
            margin-top: 30px;
            margin-bottom: 15px;
            color: #667eea;
        }
        
        h1 { font-size: 2em; }
        h2 { font-size: 1.7em; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; }
        h3 { font-size: 1.4em; }
        h4 { font-size: 1.2em; }
        
        p {
            margin-bottom: 15px;
        }
        
        ul, ol {
            margin-left: 30px;
            margin-bottom: 15px;
        }
        
        li {
            margin-bottom: 8px;
        }
        
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #d63384;
        }
        
        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin-bottom: 15px;
            font-family: 'Courier New', monospace;
        }
        
        pre code {
            background: none;
            color: inherit;
            padding: 0;
        }
        
        blockquote {
            border-left: 4px solid #667eea;
            padding-left: 15px;
            margin: 20px 0;
            color: #666;
            font-style: italic;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        
        table th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
        }
        
        table td {
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        table tr:hover {
            background: #f9f9f9;
        }
        
        a {
            color: #667eea;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
            color: #764ba2;
        }
        
        .button {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            margin-top: 20px;
            transition: transform 0.2s;
        }
        
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }
        
        .toc {
            background: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 30px;
        }
        
        .toc h2 {
            margin-top: 0;
            border: none;
            padding-bottom: 0;
        }
        
        .toc ul {
            margin-left: 20px;
        }
        
        .back-to-top {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 0.9em;
            margin-top: 30px;
        }
        
        @media (max-width: 768px) {
            header h1 { font-size: 1.8em; }
            nav ul { flex-direction: column; gap: 10px; }
            main { padding: 20px; }
        }
    </style>
    """
    
    @staticmethod
    def markdown_to_html(content):
        """Convert Markdown to HTML"""
        # Headers
        content = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
        content = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
        content = re.sub(r'^##### (.*?)$', r'<h5>\1</h5>', content, flags=re.MULTILINE)
        content = re.sub(r'^###### (.*?)$', r'<h6>\1</h6>', content, flags=re.MULTILINE)
        
        # Bold
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'__(.*?)__', r'<strong>\1</strong>', content)
        
        # Italic
        content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
        content = re.sub(r'_(.*?)_', r'<em>\1</em>', content)
        
        # Links
        content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', content)
        
        # Code blocks
        content = re.sub(r'```(.*?)\n(.*?)```', r'<pre><code>\2</code></pre>', content, flags=re.DOTALL)
        
        # Inline code
        content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)
        
        # Unordered lists
        lines = content.split('\n')
        in_list = False
        result = []
        for line in lines:
            if re.match(r'^\* ', line) or re.match(r'^- ', line):
                if not in_list:
                    result.append('<ul>')
                    in_list = True
                result.append('<li>' + re.sub(r'^[\*-] ', '', line) + '</li>')
            elif re.match(r'^\d+\. ', line):
                if in_list:
                    result.append('</ul>')
                    in_list = False
                result.append('<li>' + re.sub(r'^\d+\. ', '', line) + '</li>')
            else:
                if in_list:
                    result.append('</ul>')
                    in_list = False
                result.append(line)
        
        if in_list:
            result.append('</ul>')
        
        content = '\n'.join(result)
        
        # Blockquotes
        content = re.sub(r'^> (.*?)$', r'<blockquote>\1</blockquote>', content, flags=re.MULTILINE)
        
        # Paragraphs
        paragraphs = re.split(r'\n\n+', content)
        paragraphs = [f'<p>{p}</p>' if p and not re.match(r'^<[h|u|o|b|pre]', p) else p for p in paragraphs]
        content = '\n'.join(paragraphs)
        
        return content
    
    def generate_index(self):
        """Generate index.html"""
        nav_links = '\n'.join([
            f'<li><a href="{file.replace(".md", ".html")}">{file.replace(".md", "")}</a></li>'
            for file in self.MARKDOWN_FILES
        ])
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini-GTA Documentation</title>
    {self.CSS_STYLE}
</head>
<body>
    <div class="container">
        <header>
            <h1>🎮 Mini-GTA</h1>
            <p class="subtitle">Complete Documentation Portal</p>
        </header>
        
        <nav>
            <ul>
                {nav_links}
            </ul>
        </nav>
        
        <main>
            <h2>Welcome to Mini-GTA Documentation</h2>
            <p>This is the central hub for all Mini-GTA documentation. Select any guide from the navigation menu above to get started.</p>
            
            <h3>Available Guides</h3>
            <ul>
                <li><strong>APK Quickstart</strong> - Quick setup guide for the APK</li>
                <li><strong>Clock README</strong> - Clock feature documentation</li>
                <li><strong>Deployment Checklist</strong> - Pre-deployment verification steps</li>
                <li><strong>Deployment Summary</strong> - Complete deployment guide</li>
                <li><strong>Enhancement Plan</strong> - Planned enhancements and features</li>
                <li><strong>Final Status</strong> - Project completion status</li>
                <li><strong>How to Play</strong> - Game mechanics and controls</li>
                <li><strong>How to Play Guide</strong> - Detailed gameplay guide</li>
            </ul>
            
            <div class="toc">
                <h2>Quick Navigation</h2>
                <ul>
                    {nav_links}
                </ul>
            </div>
        </main>
        
        <footer>
            <p>Mini-GTA Documentation | Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
</body>
</html>
"""
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("✓ Generated: index.html")
    
    def generate_from_markdown(self, md_file):
        """Generate HTML from a Markdown file"""
        if not os.path.exists(md_file):
            print(f"✗ File not found: {md_file}")
            return
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert markdown to HTML
        html_content = self.markdown_to_html(content)
        
        # Generate navigation
        nav_links = '\n'.join([
            f'<li><a href="{file.replace(".md", ".html")}">{file.replace(".md", "")}</a></li>'
            for file in self.MARKDOWN_FILES
        ])
        
        html_filename = md_file.replace('.md', '.html')
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{md_file.replace('.md', '')} - Mini-GTA</title>
    {self.CSS_STYLE}
</head>
<body>
    <div class="container">
        <header>
            <h1>🎮 Mini-GTA</h1>
            <p class="subtitle">{md_file.replace('.md', '')}</p>
        </header>
        
        <nav>
            <ul>
                <li><a href="index.html">Home</a></li>
                {nav_links}
            </ul>
        </nav>
        
        <main>
            {html_content}
            <a href="index.html" class="back-to-top">← Back to Home</a>
        </main>
        
        <footer>
            <p>Mini-GTA Documentation | Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
</body>
</html>
"""
        
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✓ Generated: {html_filename}")
    
    def generate_all(self):
        """Generate all HTML files"""
        print("=" * 60)
        print("Mini-GTA HTML Generator")
        print("=" * 60)
        
        # Generate index
        self.generate_index()
        
        # Generate individual pages
        for md_file in self.MARKDOWN_FILES:
            self.generate_from_markdown(md_file)
        
        print("=" * 60)
        print("✓ All HTML files generated successfully!")
        print("=" * 60)
        print("\nGenerated files:")
        print("  - index.html (Main page)")
        for md_file in self.MARKDOWN_FILES:
            print(f"  - {md_file.replace('.md', '.html')}")


def main():
    """Main entry point"""
    generator = HTMLGenerator()
    generator.generate_all()


if __name__ == '__main__':
    main()
