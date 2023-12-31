from flask import Flask, request, jsonify
from ortools.linear_solver import pywraplp

app = Flask(__name__)

@app.route('/cutlist', methods=['POST'])
def cutlist_handler():
    # Read the input data from the request body
    json_input = request.json
    data = {}
    data['sourceSize'] = json_input['sourceSize']
    data['cuts'] = json_input['cuts']

    weights = []
    for cut in data['cuts']:
        length = cut['length']
        quantity = cut['quantity']
        weights.extend([length] * quantity)

    data['weights'] = weights
    data['items'] = list(range(len(weights)))
    data['bins'] = data['items']
    data['bin_capacity'] = json_input['sourceSize']

    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    x = {}
    for i in data['items']:
        for j in data['bins']:
            x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))

    y = {}
    for j in data['bins']:
        y[j] = solver.IntVar(0, 1, 'y[%i]' % j)

    # Constraints
    for i in data['items']:
        solver.Add(sum(x[i, j] for j in data['bins']) == 1)

    for j in data['bins']:
        solver.Add(
            sum(x[(i, j)] * data['weights'][i] for i in data['items']) <= y[j] *
            data['bin_capacity'])

    # Objective
    solver.Minimize(solver.Sum([y[j] for j in data['bins']]))

    status = solver.Solve()

    output = {}
    if status == pywraplp.Solver.OPTIMAL:
        num_bins = 0
        cuts = []
        for j in data['bins']:
            if y[j].solution_value() == 1:
                bin_items = []
                bin_weight = 0
                for i in data['items']:
                    if x[i, j].solution_value() > 0:
                        bin_items.append(data['weights'][i])
                        bin_weight += data['weights'][i]
                if bin_items:
                    num_bins += 1
                    for k, length in enumerate(bin_items):
                        cuts.append({'board': j+1, 'cut': k+1, 'length': length})
        output['BoardsNeeded'] = num_bins
        output['cuts'] = cuts
    else:
        output['Boards Needed'] = 0
        output['cuts'] = []
        output['message'] = 'The problem does not have an optimal solution.'

    json_output = jsonify(output)
    print(json_output)
    return json_output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
