import json
import numpy as np
import pandas as pd

# EACH JSON file has 24 entries or hours, and each file is for different city
def load_data(path):
    with open(path, 'r') as f:
        dict = json.loads(f.read())
    return dict

def get_weather(json_dict):
    results = {}
    results["id"] = json_dict[0]["city"].lower().strip()
    results ["weather_text"] = []
    results["temperature"] = []
    for weather in json_dict:
        if weather is None:
            continue

        weather_text = weather["WeatherText"].lower().strip()
        results["weather_text"].append(weather_text)

        temperature = weather["Temperature"]
        # Metric and imperial
        answers = []
        for temp_unit in temperature:
            current = temperature[temp_unit]
            answers.append(current)

        results["temperature"].append(answers)


    return results

def find_topthree_results(weather_data):
    # text_data is now a list
    text_data = weather_data['weather_text']
    mem = {}
    for text in text_data:
        if text in mem:
            mem[text] += 1
            continue

        mem[text] = 1

    mem = dict(sorted(mem.items(), key=lambda item:item[1], reverse=True)[:3])

    return list(mem.keys())

def find_average_temperature(weather_data):
    # It's a list of 2 dictionaries for C and F
    temp_data = weather_data['temperature']
    average_temp = {}

    holder_celcius = []
    holder_fahrenheit = []
    for temp in temp_data:
        holder_celcius.append(float(temp[0]['Value']))
        holder_fahrenheit.append(float(temp[1]['Value']))
        
    average_temp['C'] = np.mean(holder_celcius)
    average_temp['F'] = np.mean(holder_fahrenheit)

    return average_temp

def save_data(end_results):
    df = pd.DataFrame(end_results)
    # print(df.columns)
    df.to_csv('results.csv')
    
    
def main():
    end_results = []
    for i in range(0, 7):
        data = load_data('./data/{i}.json'.format(i=i))
        weather_data = get_weather(data)

        id = weather_data['id']
        three_results = find_topthree_results(weather_data)
        average_temperature = find_average_temperature(weather_data)

        output = {}
        output['id'] = id
        output['top_three'] = three_results
        output['average'] = average_temperature

        end_results.append(output)

    save_data(end_results)


main()


# print(get_weather(data))
# print(len(get_weather(data)['weather_text'])) -> 24