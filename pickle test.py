import pickle

listaA = [460965505222574102, 691056194852487229]

with open('channels.pickle', 'wb') as handle:
	pickle.dump(listaA, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('channels.pickle', 'rb') as handle:
    listaB = pickle.load(handle)

print(listaB)