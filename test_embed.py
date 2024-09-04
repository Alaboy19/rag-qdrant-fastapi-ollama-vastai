import json 
from fastembed import TextEmbedding


model = TextEmbedding(model_name="nomic-ai/nomic-embed-text-v1")
q1 = "I want to get a mortgage, I want to buy an apartment, I have money - how can I use it? What is financial literacy, give an example.", "https://youtu.be/TsUoHsMPamg"
q2 = "Where can I see Dividends and Coupons from my investment? Receipt and reporting. About statistics of shares.", "https://youtu.be/s_Zt-JDCH2E"
q3 = "What is the 'w8ben' form? how do we fill it?", "https://youtu.be/EwhZze4kklE"
q4 = "Where can I see the share structure in the ETF?", "https://youtu.be/82jIBRbdZYU"
q5 = "About stock exchanges in Kazakhstan and their differences, namely about 'KASE', 'AIX', 'KASE global'", "https://youtu.be/LlBxeMHXHS4"
q6 = "Info about how to exchange kz tenge to dollars and how to exchange currency on 'tradernet global'", "https://youtu.be/_iGl0P1WZJE"
q7 = "Should you switch to a standard tariff, the most suitable tariff, about the tariffs on 'tradernet global'", "https://youtu.be/JRvemzK1Tvc"
q8 = "What is the best way to buy Caspian shares? Is it better to buy Caspian shares in tenge or in dollars? What is the difference between buying shares with dollars or tenge? Depositary receipt.", "https://youtu.be/QZgXsQPnRqI"
q9 = "when the markets are open and when you can buy stocks", "https://youtu.be/MxAfIW7o9CE"
q10 = "Difference between bond coupon and stock dividend payment dates", "https://youtu.be/4nTDpLhVmSE"
qv1 = next(model.embed(q1[0]))
qv2 = next(model.embed(q2[0]))
qv3 = next(model.embed(q3[0]))
qv4 = next(model.embed(q4[0]))
qv5 = next(model.embed(q5[0]))
qv6 = next(model.embed(q6[0]))
qv7 = next(model.embed(q7[0]))
qv8 = next(model.embed(q8[0]))
qv9 = next(model.embed(q9[0]))
qv10 = next(model.embed(q10[0]))
print(type(qv1))


mypoints_save = []


a = {"id": 1, "vector": qv1.tolist(), 
                "payload": {"summary": q1[0], 
                            "url": q1[1]}
            }
mypoints_save.append(a)

b = {"id": 2, "vector": qv2.tolist(), 
                "payload": {"summary": q2[0], 
                            "url": q2[1]}
            }
mypoints_save.append(b)

c = {"id": 3, "vector": qv3.tolist(), 
                "payload": {"summary": q3[0], 
                            "url": q3[1]}
            }
mypoints_save.append(c)

d = {"id": 4, "vector": qv4.tolist(), 
                "payload": {"summary": q4[0], 
                            "url": q4[1]}
            }
mypoints_save.append(d)

e = {"id": 5, "vector": qv5.tolist(), 
                "payload": {"summary": q5[0], 
                            "url": q5[1]}
            }
mypoints_save.append(e)

f = {"id": 6, "vector": qv6.tolist(), 
                "payload": {"summary": q6[0], 
                            "url": q6[1]}
            }
mypoints_save.append(f)

h = {"id": 7, "vector": qv7.tolist(), 
                "payload": {"summary": q7[0], 
                            "url": q7[1]}
            }
mypoints_save.append(h)

j = {"id": 8, "vector": qv8.tolist(), 
                "payload": {"summary": q8[0], 
                            "url": q8[1]}
            }
mypoints_save.append(j)

k = {"id": 9, "vector": qv9.tolist(), 
                "payload": {"summary": q9[0], 
                            "url": q9[1]}
            }
mypoints_save.append(k)

l = {"id": 10, "vector": qv10.tolist(), 
                "payload": {"summary": q10[0], 
                            "url": q10[1]}
            }
mypoints_save.append(l)



with open("my_collection_video_new.json", "w") as f:
    json.dump(mypoints_save, f)
