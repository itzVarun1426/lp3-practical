#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
using namespace std;

// Deterministic Quick Sort
int partitionDet(vector<int>& a, int low, int high, long long& comparisons){
    int pivot = a[high];
    int i = low - 1;

    for (int j = low; j < high; j++){
        comparisons++;

        if (a[j] <= pivot){
            i++;
            swap(a[i], a[j]);
        }
    }

    swap(a[i + 1], a[high]);
    return i + 1;
}

void deterministicQuickSort(vector<int>& a, int low, int high,
                            long long& comparisons) {
    if (low < high){
        int pi = partitionDet(a, low, high, comparisons);

        deterministicQuickSort(a, low, pi - 1, comparisons);
        deterministicQuickSort(a, pi + 1, high, comparisons);
    }
}

// Randomized Quick Sort
int partitionRandom(vector<int>& a, int low, int high,
                    long long& comparisons, mt19937& rng){
    uniform_int_distribution<int> dist(low, high);
    int randomIndex = dist(rng);

    swap(a[randomIndex], a[high]);

    int pivot = a[high];
    int i = low - 1;

    for (int j = low; j < high; j++){
        comparisons++;

        if (a[j] <= pivot){
            i++;
            swap(a[i], a[j]);
        }
    }

    swap(a[i + 1], a[high]);
    return i + 1;
}

void randomizedQuickSort(vector<int>& a, int low, int high,
                         long long& comparisons, mt19937& rng){
    if (low < high){
        int pi = partitionRandom(a, low, high, comparisons, rng);

        randomizedQuickSort(a, low, pi - 1, comparisons, rng);
        randomizedQuickSort(a, pi + 1, high, comparisons, rng);
    }
}

// Display array
void display(vector<int>& a){
    for (int x : a)
        cout << x << " ";
    cout << endl;
}

int main(){
    int n;
    cout << "Enter number of elements: ";
    cin >> n;

    vector<int> a(n);

    cout << "Enter array elements: ";
    for (int i = 0; i < n; i++)
        cin >> a[i];

    vector<int> b = a;

    long long detComparisons = 0;
    long long randComparisons = 0;

    mt19937 rng(random_device{}());

    // Deterministic Quick Sort
    deterministicQuickSort(a, 0, n - 1, detComparisons);

    // Randomized Quick Sort
    randomizedQuickSort(b, 0, n - 1, randComparisons, rng);

    cout << "\nDeterministic Quick Sort:\n";
    display(a);
    cout << "Number of comparisons: " << detComparisons << endl;

    cout << "\nRandomized Quick Sort:\n";
    display(b);
    cout << "Number of comparisons: " << randComparisons << endl;
}
