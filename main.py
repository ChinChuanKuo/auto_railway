def solution_website(json):
    from selenium import webdriver
    from selenium.webdriver.support.ui import Select
    from time import sleep
    json_data = json["info"]
    url = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    driver.find_element_by_xpath("//input[@id='pid']").send_keys(json_data["idcard"])
    driver.find_element_by_xpath("//input[@id='startStation']").send_keys(json_data["start_station"])
    driver.find_element_by_xpath("//input[@id='endStation']").send_keys(json_data["end_station"])
    if json_data["type"] != "單程":
        #driver.execute_script("arguments[0].setAttribute('class','btn btn-lg btn-linear')", driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear active'])[1]"))
        #driver.execute_script("arguments[0].setAttribute('class','btn btn-lg btn-linear active')", driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear'])[2]"))
        driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear'])[1]").click()
    if json_data["way"] != "依車次":
        #driver.execute_script("arguments[0].setAttribute('class','btn btn-lg btn-linear')", driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear active'])[2]"))
        #driver.execute_script("arguments[0].setAttribute('class','btn btn-lg btn-linear active')", driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear'])[3]"))
        driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear'])[2]").click()
    normalQty = driver.find_element_by_xpath("//input[@id='normalQty']")
    normalQty.clear()
    normalQty.send_keys(json_data["count"])
    if json_data["type"] == "單程":
        single_data = json_data["single"]
        if json_data["way"] == "依車次":
            driver.find_element_by_xpath("//input[@id='rideDate1']").send_keys(single_data["car"]["date"])
            train_list = 0
            while (train_list < 3):
                driver.find_element_by_xpath("//input[@id='trainNoList"+str(train_list+1)+"']").send_keys(single_data["car"]["train_number"][str(train_list)])
                train_list+=1
            if single_data["car"]["seat_preference"] != "不指定":
                driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear tableFirst'])[1]").click()
            #if single_data["car"]["search_preference"] != "Yes":
            #    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear active'])[5]"))
        else:
            driver.find_element_by_xpath("//input[@id='rideDate1']").send_keys(single_data["time"]["date"])
            startTime = driver.find_element_by_xpath("//select[@id='startTime1']")
            for option in startTime.find_elements_by_tag_name('option'):
                if option.text == single_data["time"]["time_period"]["start_time"]:
                    option.click()
                    break
            endTime = driver.find_element_by_xpath("//select[@id='endTime1']")
            for option in endTime.find_elements_by_tag_name('option'):
                if option.text == single_data["time"]["time_period"]["end_time"]:
                    option.click()
                    break
            if single_data["time"]["seat_preference"] != "不指定":
                driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear tableFirst'])[1]").click()
            car_type = 0
            ele_count = 3
            while (car_type < 5):
                if single_data["time"]["car_type"][str(car_type)] == "Yes":
                    driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear'])["+str(ele_count)+"]").click()
                else:
                    ele_count+=1
                car_type+=1
            if single_data["time"]["discount"] == "Yes":
                driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear '])[1]").click()
    else:
        comback_data = json_data["comeback"]
        if json_data["way"] == "依車次":
            #去程
            driver.find_element_by_xpath("//input[@id='rideDate1']").send_keys(comback_data["car"]["go"]["date"])
            train_list = 0
            while (train_list < 3):
                driver.find_element_by_xpath("//input[@id='trainNoList"+str(train_list+1)+"']").send_keys(comback_data["car"]["go"]["train_number"][str(train_list)])
                train_list+=1
            table_first = 1
            if comback_data["car"]["go"]["seat_preference"] != "不指定":
                driver.execute_script("arguments[0].click();", driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear tableFirst'])["+str(table_first)+"]"))
            else:
                table_first+=1
            #回程
            driver.find_element_by_xpath("//input[@id='rideDate2']").send_keys(comback_data["car"]["back"]["date"])
            train_list = 0
            while (train_list < 3):
                driver.find_element_by_xpath("//input[@id='trainNoList"+str(train_list+1)+"']").send_keys(comback_data["car"]["back"]["train_number"][str(train_list)])
                train_list+=1
            if comback_data["car"]["back"]["seat_preference"] != "不指定":
                driver.execute_script("arguments[0].click();", driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear tableFirst'])["+str(table_first)+"]"))
        else:
            #去程
            driver.find_element_by_xpath("//input[@id='rideDate1']").send_keys(comback_data["time"]["go"]["date"])
            startTime = driver.find_element_by_xpath("//select[@id='startTime1']")
            for option in startTime.find_elements_by_tag_name('option'):
                if option.text == comback_data["time"]["go"]["time_period"]["start_time"]:
                    option.click()
                    break
            endTime = driver.find_element_by_xpath("//select[@id='endTime1']")
            for option in endTime.find_elements_by_tag_name('option'):
                if option.text == comback_data["time"]["go"]["time_period"]["end_time"]:
                    option.click()
                    break
            table_first = 1
            if comback_data["time"]["go"]["seat_preference"] != "不指定":
                driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear tableFirst'])["+str(table_first)+"]").click()
            else:
                table_first+=1
            car_type = 0
            ele_count = 3
            while (car_type < 5):
                if comback_data["time"]["go"]["car_type"][str(car_type)] == "Yes":
                    driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear'])["+str(ele_count)+"]").click()
                else:
                    ele_count+=1
                car_type+=1
            discount = 1
            if comback_data["time"]["go"]["discount"] == "Yes":
                driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear '])["+str(discount)+"]").click()
            else:
                discount+=1
            #回程
            driver.find_element_by_xpath("//input[@id='rideDate2']").send_keys(comback_data["time"]["back"]["date"])
            startTime = driver.find_element_by_xpath("//select[@id='startTime2']")
            for option in startTime.find_elements_by_tag_name('option'):
                if option.text == comback_data["time"]["back"]["time_period"]["start_time"]:
                    option.click()
                    break
            endTime = driver.find_element_by_xpath("//select[@id='endTime2']")
            for option in endTime.find_elements_by_tag_name('option'):
                if option.text == comback_data["time"]["back"]["time_period"]["end_time"]:
                    option.click()
                    break
            if comback_data["time"]["back"]["seat_preference"] != "不指定":
                driver.execute_script("arguments[0].click();", driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear tableFirst'])["+str(table_first)+"]"))
            car_type = 0
            while (car_type < 5):
                if comback_data["time"]["back"]["car_type"][str(car_type)] == "Yes":
                    driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear'])["+str(ele_count)+"]").click()
                else:
                    ele_count+=1
                car_type+=1
            if comback_data["time"]["back"]["discount"] == "Yes":
                driver.find_element_by_xpath("(//label[@class='btn btn-lg btn-linear '])["+str(discount)+"]").click()
    sleep(10)
    driver.find_element_by_xpath("//label[@id='submitBtn']").click()

def get_json():
    import json
    with open("main.json", "r") as f:
        data = json.load(f)
        return data

if __name__ == "__main__":
    solution_website(get_json())