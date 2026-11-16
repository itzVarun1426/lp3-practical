#include <iostream>
#include <algorithm>
using namespace std;

struct Item {
    int weight;
    int profit;
    double ratio;
};

// Compare items according to profit/weight ratio
bool compare(Item a, Item b) {
    return a.ratio > b.ratio;
}

int main() {
    int n, capacity;
    cout << "Enter number of items: ";
    cin >> n;

    Item items[n];

    cout << "Enter weight and profit of each item:\n";

    for (int i = 0; i < n; i++) {
        cin >> items[i].weight >> items[i].profit;

        items[i].ratio =
            (double)items[i].profit / items[i].weight;
    }

    cout << "Enter knapsack capacity: ";
    cin >> capacity;

    // Sort items in descending order of ratio
    sort(items, items + n, compare);

    double totalProfit = 0;

    // Apply Greedy Method
    for (int i = 0; i < n; i++) {

        if (capacity == 0)
            break;

        // If complete item can fit
        if (items[i].weight <= capacity) {

            capacity -= items[i].weight;
            totalProfit += items[i].profit;
        }

        // If only a fraction can fit
        else {

            double fraction =
                (double)capacity / items[i].weight;

            totalProfit += items[i].profit * fraction;

            capacity = 0;
        }
    }

    cout << "\nMaximum Profit = " << totalProfit;
}
