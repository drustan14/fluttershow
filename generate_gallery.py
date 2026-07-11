import os
import re
from datetime import datetime

TEMPLATE_FILE = "template.html"
OUTPUT_FILE = "build/deploy_site/index.html"
PROJECTS_DIR = "projects"

def parse_project_metadata(project_path, folder_name):
    app_name = folder_name
    version = "1.0.0"
    description = "暂无项目描述，请在 pubspec.yaml 中填写 description。"

    main_dart_path = os.path.join(project_path, "lib", "main.dart")
    if os.path.exists(main_dart_path):
        with open(main_dart_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            match = re.search(r'title\s*:\s*[\'"]([^\'"]+)[\'"]', content)
            if match:
                app_name = match.group(1)

    pubspec_path = os.path.join(project_path, "pubspec.yaml")
    if os.path.exists(pubspec_path):
        with open(pubspec_path, "r", encoding="utf-8", errors="ignore") as f:
            pub_content = f.read()
            v_match = re.search(r'^version:\s*([^\s\n]+)', pub_content, re.MULTILINE)
            if v_match:
                version = v_match.group(1).split('+')[0]
            d_match = re.search(r'^description:\s*([^\n]+)', pub_content, re.MULTILINE)
            if d_match:
                description = d_match.group(1).strip().strip('"').strip("'")

    return app_name, version, description

def main():
    if not os.path.exists(PROJECTS_DIR):
        print(f"❌ 错误: 未找到 {PROJECTS_DIR} 文件夹")
        return

    project_cards = []
    project_count = 0
    
    for folder in sorted(os.listdir(PROJECTS_DIR)):
        project_path = os.path.join(PROJECTS_DIR, folder)
        if os.path.isdir(project_path) and os.path.exists(os.path.join(project_path, "pubspec.yaml")):
            project_count += 1
            app_name, version, description = parse_project_metadata(project_path, folder)
            
            android_svg = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>'
            web_svg = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'

            card_html = f"""
            <div class="project-card">
                <div class="card-header">
                    <div class="app-icon-wrapper">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
                    </div>
                    <span class="version-badge">v{version}</span>
                </div>
                <h3>{app_name}</h3>
                <p class="project-desc">{description}</p>
                <div class="card-actions">
                    <a href="./web_subprojects/{folder}/index.html" class="btn btn-web">{web_svg} 在线预览</a>
                    <a href="./downloads/{folder}-arm64.apk" class="btn btn-apk">{android_svg} 下载 APK</a>
                </div>
            </div>
            """
            project_cards.append(card_html)

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template_content = f.read()

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    final_html = template_content.replace("", "\n".join(project_cards))
    final_html = final_html.replace("", str(project_count))
    final_html = final_html.replace("", current_date)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"🚀 成功动态生成包含 {project_count} 个项目的展示面板！")

if __name__ == "__main__":
    main()