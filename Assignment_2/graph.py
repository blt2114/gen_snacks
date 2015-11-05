from pylab import *
import sys

def pie_chart(data):
    ingredients = [o[0] for o in data]
    frequency = [f[1] for f in data]
    total = sum(frequency)
    proportion = [f*100/float(total) for f in frequency]

    figure(1, figsize=(6,6))
    ax = axes([0.1, 0.1, 0.8, 0.8])
    pie(proportion, labels=ingredients, autopct='%1.1f%%', shadow=True, startangle=90)
    title('Ingredients in Dish', bbox={'facecolor':'0.8', 'pad':5})
    return savefig('ingredient_pieChart.png', bbox_inches='tight')

def main():
    data = []
    if len(sys.argv) > 1:
	if type(sys.argv[1]) == list:
            data = sys.argv[1]
        else:
            print "Error: Second argument is not a list of tuples"
    else:
        print "Error: graph.py requires data passed in as a second argument"
        #data = [('apple', 1), ('orange', 2), ('pear',3)]
    pie_chart(data)

if __name__ == "__main__": main()
