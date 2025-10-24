from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyperclip

class LOCAL_API():
    def __init__(self):
        self.history = {'last_prompt_no': -1, 'last_response_id': None}
        self.__init__driver()
        
    def create_web_driver(self, position_x=1920, position_y=0, size_x=1400, size_y=600):
        options = webdriver.ChromeOptions()
        # Set Chrome options to block images, CSS, fonts, etc.
        chrome_prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.stylesheets": 2,
            "profile.managed_default_content_settings.fonts": 2,
            "profile.managed_default_content_settings.plugins": 2,
            "profile.managed_default_content_settings.popups": 2,
            "profile.managed_default_content_settings.geolocation": 2,
            "profile.managed_default_content_settings.notifications": 2,
        }
        options.add_experimental_option("prefs", chrome_prefs)
        # options.add_argument("--headless")  # Run headless if you don't need a visible browser
        # options.add_argument('--start-maximized')  # maximized window
        # Set window size: width=800px, height=600px
        options.add_argument(f"--window-size={size_x},{size_y}")
        # Set window position: x=100px from left, y=50px from top
        options.add_argument(f"--window-position={position_x},{position_y}")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        # Initialize driver
        # return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return webdriver.Chrome(service=Service(r"C:\Chrome_Driver\chromedriver.exe"), options=options)
    
    def __init__driver(self, delay=0.5):
        self.driver = self.create_web_driver()
        self.creation_time = time.time()
        self.driver.get("https://gemini.google.com/app")
        time.sleep(delay)  # wait for page to load

    def quit_driver(self):
        self.driver.quit()
    
    def restart_driver(self):
        try:
            self.quit_driver()
        except: pass
        self.__init__driver()
    
    def clear_history(self):
        self.history = {'last_prompt_no': -1, 'last_response_id': None}

    def get_prompt_box(self):
        return self.driver.find_element(By.XPATH, '//div[@role="textbox" and @aria-label="Enter a prompt here"]')

    def get_send_button(self):
        return self.driver.find_element(By.XPATH, '//button[contains(@class, "send-button")]')# Click the button

    def send_prompt(self, msg, delay=0.01):
        # Locate the element using XPath
        try:
            text_box = self.get_prompt_box()
            # lines = msg.split('\n')   ## method 1 takes time: slow and lazy
            # for i, line in enumerate(lines):
            #     text_box.send_keys(line)
            #     if i < len(lines) - 1:
            #         text_box.send_keys(Keys.SHIFT, Keys.ENTER)

            # pyperclip.copy(msg)      ## method 2: faster: but disturbs clipboard. risky.
            # text_box.click()
            # text_box.send_keys(Keys.CONTROL, 'v')  # paste entire text
            ## method 3: fastest and efficient: does not disturb clipboard, does not need click
            # self.driver.execute_script("arguments[0].innerText = arguments[1];", text_box, msg)
            self.driver.execute_script("arguments[0].textContent = arguments[1];", text_box, msg.rstrip('\n'))
        except Exception as e:
            return f"Error occurred while sending prompt: {e}"
        # print("Prompt sent to box") # delete later
        # time.sleep(delay)  ## no need to wait here
        err = "Button not found: timeout"
        start_time = time.time()
        while (time.time() - start_time) < 3:  # timeout after 3 seconds
            # print("Trying to find button") # delete later
            try:
                button = self.get_send_button()
                label = button.get_attribute("aria-label")
                if "Send" in label:
                    button.click()
                    self.history['last_prompt_no'] += 1
                    self.history[self.history['last_prompt_no']] = {'prompt': msg, 'response': None}
                    return "Prompt sent and button clicked successfully"
                # elif "Stop" in label:
                #     print("This is the Stop button")
            except Exception as e:
                err = e
            time.sleep(0.1)  # Wait before trying again
        return f"Error occurred while clicking button: {err}"
    
    def get_last_response(self):  
        err, div_text, new_response_id = None, None, False
        try:
            button = self.get_send_button()
            label = button.get_attribute("aria-label")
            if "Stop" in label:
                return {'response': None, 'error': 'still generating', 'id': None}
        except:
            pass

        try: 
            response_containers = self.driver.find_elements(
                By.XPATH, 
                "//div[starts-with(@class, 'conversation-container')]"
            )
            new_response_id = response_containers[-1].get_attribute("id")
            if new_response_id == self.history['last_response_id'] and self.history['last_response_id']:
                return {'response': None, 'error': 'no new response', 'id': None}
            
            div_elements = response_containers[-1].find_elements(
                By.XPATH,
                ".//message-content[starts-with(@class,'model-response-text')]"
            )
            div_text = div_elements[-1].text
        except Exception as e:
            err = e
        response = {'response': div_text, 'error': err, 'id':  new_response_id if new_response_id else None}
        if new_response_id:
            self.history[self.history['last_prompt_no']]['response'] = response
            self.history['last_response_id'] = new_response_id
        return response
    
    def copy_last_response_to_clipboard(self):
        pass
        # steps: same as get_last_response, then find the copy button and click it
        # try:
        #     <button _ngcontent-ng-c4159091283 mat-button tabindex="0" mattooltip="Copy response" aria-label="Copy" data-test-id="copy-button" class="mdc-button mat-mdc-button-base mat-mdc-tooltip-trigger icon-button mat-mdc-button mat-unthemed" mat-ripple-loader-class-name="mat-mdc-button-ripple" jslog="178035;track:generic_click,impression;BardVeMetadataKey:[["r_7711edcb96c84e21","c_a39913e6d4337352",null,"rc_c5681538456025e4",null,null,"en",null,1,null,null,1,0]];mutable:true" aria-describedby="cdk-describedby-message-ng-1-11" cdk-describedby-host="ng-1">flex
        # except Exception as e:
        #     return f"Error occurred while copying to clipboard: {e}"

    def execute_prompt(self, prompt, inertial_delay=0.4, timeout=30):
        send_status = self.send_prompt(prompt)
        response = {'response': None, 'error': None, 'id': None}
        result = {'prompt': prompt, 'response': response}
        # print(send_status)
        if "Error" in send_status:
            result['response']['error'] = send_status
            return result
        
        time.sleep(inertial_delay)
        result['response']['error'] = "timeout after sending prompt"
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            response = self.get_last_response()
            if response['error'] == 'still generating':
                time.sleep(0.2)
                continue
            elif response['error'] == 'no new response':
                time.sleep(0.2)
                continue
            else:
                result['response'] = response
                break
        return result

    def execute_prompts(self, prompts, inertial_delay=0.4, timeout=30, delay_between_prompts=0.4):
        results = []
        for prompt in prompts:
            result = self.execute_prompt(prompt, inertial_delay, timeout)
            results.append(result)
            if result['response']['error'] and 'timeout' in result['response']['error']:
                break
            time.sleep(delay_between_prompts)
        return results

  
if __name__ == "__main__":
    pass
    # api = LOCAL_API()
    # # response = api.send_prompt("Hello, how are you?")
    # # print(response)
    # # time.sleep(2)
    # # response = api.get_last_response()
    # # print(response)
    # hard_math_prompts = [
    #     "What is 123456789 * 987654321?",
    #     "What is 34/7 + 56/9?",
    # ]
    # results = api.execute_prompts(hard_math_prompts)
    # for res in results:
    #     print(res['response']['response'])
    # time.sleep(20)
    # api.quit_driver()
    # del api