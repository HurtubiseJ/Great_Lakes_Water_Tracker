import matplotlib.pyplot as plt
import API_Pulls.info_pull as APIPull

def createLineGraph(response):
    list = format_response(response)
    fig, ax = plt.subplots()
    ax.plot()

#TODO: Dimnsions need to be flipped all dates in a list, all vals in a list
def format_response(response):
    list = []
    for row in response:
        list.append([row[0], row[1]])
    return list

def main():
    response = APIPull.exec_select_range('9034052', '2024-08-26 00:00:00.000', '2024-08-26 00:54:00.000')

    pass

if __name__ == '__main__':
    main()