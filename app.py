from flask import Flask, request
from flask_cors import CORS
import requests
import json
import constant

app = Flask(__name__)
CORS(app)


@app.route('/create_phrase', methods=['POST'])
def create_phrase():  # put application's code here
    data = request.get_json()
    # if True:
    #     return "THis is very log success messsssssssssssssssssss", 200
    if not data:
        return 'No parameter found', 400
    if 'zipcode' not in data:
        return 'zipcode parameter not found', 400
    if 'first_name' not in data:
        return 'first_name parameter not found', 400
    if 'last_name' not in data:
        return 'last_name parameter not found', 400
    zipcode, first_name, last_name = data
    print(data)
    print('zipcode' + zipcode)
    county_response = requests.get('https://service.zipapi.us/zipcode/county/' + zipcode
                            + '?X-API-KEY=' + constant.API_KEY,
                            auth=(constant.USERNAME, constant.PASSWORD))
    county_json = json.loads(county_response.content)
    print(county_json)
    if not county_json['status']:
        return county_json['message'], 404
    county = county_json["data"]["county"][0];

    zipcode_response = requests.get('https://service.zipapi.us/population/zipcode/' + zipcode
                     + '?X-API-KEY=' + constant.API_KEY,
                     auth=(constant.USERNAME, constant.PASSWORD))

    zipcode_json = json.loads(zipcode_response.content)
    if not zipcode_json['status']:
        return zipcode_json['message'], 404
    population = zipcode_json["data"]["population"]

    first_name = get_pig_latin(first_name).title()
    last_name = get_pig_latin(last_name).lower()
    result = first_name + " " + last_name + "'s zip code is in " + county + \
            " County and has a population of " + population

    return result, 200


def get_pig_latin(name):
    if name[0] in 'aeiou':
        name = name + "ay"
    else:
        '''
        else get vowel position and postfix all the consonants 
        present before that vowel to the end of the word along with "ay"
        '''
        has_vowel = False

        for j, letter in enumerate(name):
            if letter in 'aeiou':
                name = name[j:] + name[:j] + "ay"
                has_vowel = True
                break

        # if the word doesn't have any vowel then simply postfix "ay"

        if not has_vowel:
            name = name + "ay"

    return name


if __name__ == '__main__':
    app.run()
