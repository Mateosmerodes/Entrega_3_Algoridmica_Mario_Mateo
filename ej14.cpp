#include <iostream>
#include <vector>
#include <random>
using namespace std;

// Checks to see if item is in a vector returns true or false (1 or 0) using binary Search
bool binarySearch_iterative(vector<int> avector, int item) 
{
    int first = 0;
    int last = avector.size() - 1;
    bool found = false;

    while (first <= last && !found) 
    {
        int midpoint = (first + last) / 2;
        if (avector[midpoint] == item) 
            found = true;
        else 
            if (item < avector[midpoint]) 
                last = midpoint - 1;
            else 
                first = midpoint + 1;
    }
    return found;
}




bool binarySearch_recursive(vector <int> arr, int start, int end, int item)
{
    if (end >= start)
    {
        int mid = start + (end - start) / 2;
        if (arr[mid] == item)
            return true;
        if (arr[mid] > item)
            return binarySearch_recursive(arr, start, mid - 1, item);
        else
            return binarySearch_recursive(arr, mid + 1, end, item);
    }

    return false;
}

int main(void)
{
    srand(time(NULL));
    vector <int> arr;
    
    for (int i=0;i<=90;i++)
    {
        int num;
        num=rand()%70;
        arr.push_back(num);
    }
    for (int i=0;i<=arr.size();i++)
    {
        cout<< arr[i]<<' ';
    }
    cout << '\n';

    
    int arrLength = arr.size();
    cout <<"Búsqueda con binario recursivo:\n";
    cout <<"Búsqueda del número 3: "<< binarySearch_recursive(arr, 0, arrLength, 3) << endl;
    cout <<"Búsqueda del número 3: "<< binarySearch_recursive(arr, 0, arrLength, 13) << endl;
    
    



 

    //Using static array to initialize a vector
    
    cout <<"Búsqueda con binario iterativo:\n";

    cout <<"Búsqueda del número 3: "<< binarySearch_iterative(arr, 3) << endl;
    cout << "Búsqueda del número 13: "<<binarySearch_iterative(arr, 13) << endl;
    
    return 0;
}




