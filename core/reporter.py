import os

class HTMLReporter:
    def __init__(self, filename="report.html"):
        self.filename = filename

    def generate_report(self, vulnerabilities):
        """
        Ye function vulnerabilities ki list leta hai aur ek HTML file banata hai.
        """
        html_content = """
        <html>
        <head>
            <title>XSS Scan Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #d32f2f; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .vuln { color: red; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>XSS Vulnerability Report</h1>
            <table>
                <tr>
                    <th>URL</th>
                    <th>Context</th>
                    <th>Payload Used</th>
                    <th>Status</th>
                </tr>
        """

        # Agar koi kami nahi mili
        if not vulnerabilities:
            html_content += "<tr><td colspan='4'>No Vulnerabilities Found (Safe)</td></tr>"
        
        # Agar kami mil gayi, toh table mein row add karo
        for vuln in vulnerabilities:
            html_content += f"""
            <tr>
                <td>{vuln['url']}</td>
                <td>{vuln['context']}</td>
                <td><code>{vuln['payload'].replace('<', '&lt;').replace('>', '&gt;')}</code></td>
                <td class="vuln">VULNERABLE</td>
            </tr>
            """

        html_content += """
            </table>
        </body>
        </html>
        """

        # File save karo
        with open(self.filename, "w") as f:
            f.write(html_content)
        
        print(f"\n[+] Report generated successfully: {os.path.abspath(self.filename)}")