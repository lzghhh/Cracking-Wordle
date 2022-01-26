#!/usr/bin/env python3
import random
import socket, argparse, ssl, json

parser = argparse.ArgumentParser(description='Client Comm')
parser.add_argument('-p', '--port', type=int, metavar='', help='Server Port')
parser.add_argument('-s', '--flag', type=int, metavar='', help='Server Port')
parser.add_argument('hostname', type=str, metavar='', help='The name of the server')
parser.add_argument('username', type=str, metavar='', help='Northeastern Username')
args = parser.parse_args()

if args.port is not None:
    PORT = args.port
else:
    PORT = 27993

if args.flag is not None:
    SEVER = args.flag
    if PORT == 27993:
        PORT = 27994


hostname = args.hostname
username = args.username

address = (hostname, PORT)

file = open('./words.txt', 'r')
wordlist = file.readlines()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(address)

message_hello = {"type": "hello", "northeastern_username": "kong.weix"}
message_hello_json = json.dumps(message_hello)
message_hello_sent = (message_hello_json + "\n").encode("utf-8")
client.send(message_hello_sent)

message_start_received = client.recv(8192).decode("utf-8")
message_start_json = json.loads(message_start_received)
id = message_start_json["id"]

word_count = 0

while True:
    word = wordlist[random.randint(0, len(wordlist) - 1)]
    message_guess = {"type": "guess", "id": id, "word": word.rstrip()}
    message_guess_json = json.dumps(message_guess)
    message_guess_sent = (message_guess_json  + "\n").encode("utf-8")
    client.send(message_guess_sent)
    word_count += 1

    message_guess_receive = client.recv(8192).decode("utf-8")
    message_guess_receive_json = json.loads(message_guess_receive)

#  This part is to determine whether flag appears
    if message_guess_receive_json.get("flag", "True")  != "True":
        print(word_count)
        print("flag: " + message_guess_receive_json["flag"])
        file.close()
        break;

# This part is to find new words
    message_guess_receive_list = message_guess_receive_json["guesses"]

    feedback = message_guess_receive_list[len(message_guess_receive_list) - 1]
    for index in range(len(feedback)):
        if feedback["marks"][index] == 0:
            index1 = 0
            while index1 < len(wordlist):
                if wordlist[index1].find(word[index]) != -1:
                    wordlist.pop(index1)
                else:
                    index1 += 1
            # for index2 in range(len(wordlist)):
            #     print("2")
            #     print(index2)
            #     if wordlist[index2].find(word[index]) != -1:
            #         wordlist.pop(index2)

        elif feedback["marks"][index] == 1 :
            index2 = 0
            while index2 < len(wordlist):
                if wordlist[index2].find(word[index]) == -1:
                    wordlist.pop(index2)
                else:
                    index2 += 1
            # for index3 in range(len(wordlist)):
            #     print("3")
            #     print(index3)
            #     if wordlist[index3].find(word[index]) == -1:
            #         wordlist.pop(index3)

        else:
            index3 = 0
            while index3 < len(wordlist):
                if wordlist[index3][index] != word[index]:
                    wordlist.pop(index3)
                else:
                    index3 += 1
            # for index4 in range(len(wordlist)):
            #     print("4")
            #     print(index4)
            #     if wordlist[index4][index] != word[index]:
            #         wordlist.pop(index4)








