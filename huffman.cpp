
#include <iostream>
#include <queue>
#include <vector>
using namespace std;

class Node {
public:
    char ch;
    int freq;

    Node* left;
    Node* right;

    Node(char c, int f) {
        ch = c;
        freq = f;
        left = right = NULL;
    }
};

// Comparator for Min Priority Queue
class Compare {
public:
    bool operator()(Node* a, Node* b) {
        return a->freq > b->freq;
    }
};

class Huffman {
public:
    // Generate Huffman Codes
    void generateCodes(Node* root, string code) {

        if (root == NULL)
            return;

        // Leaf node
        if (root->left == NULL && root->right == NULL) {
            cout << root->ch << " : " << code << endl;
            return;
        }

        generateCodes(root->left, code + "0");
        generateCodes(root->right, code + "1");
    }

    // Build Huffman Tree
    void buildTree(char characters[], int freq[], int n) {

        priority_queue<Node*, vector<Node*>, Compare> pq;

        // Insert characters into priority queue
        for (int i = 0; i < n; i++) {
            pq.push(new Node(characters[i], freq[i]));
        }

        // Apply Greedy Strategy
        while (pq.size() > 1) {

            Node* left = pq.top();
            pq.pop();

            Node* right = pq.top();
            pq.pop();

            Node* newNode = new Node('$',
                                     left->freq + right->freq);

            newNode->left = left;
            newNode->right = right;

            pq.push(newNode);
        }

        // Generate codes
        cout << "\nHuffman Codes:\n";
        generateCodes(pq.top(), "");
    }
};

int main() {

    char characters[] = {'A', 'B', 'C', 'D', 'E', 'F'};
    int freq[] = {5, 9, 12, 13, 16, 45};

    int n = sizeof(characters) / sizeof(characters[0]);

    Huffman h;

    h.buildTree(characters, freq, n);
}
