function getMax(arr) {
    let max = arr[0];
    for (let i = 1; i < arr.length; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}

function countingSort(arr, exp) {
    let n = arr.length;
    let output = new Array(n).fill(0);
    let count = new Array(10).fill(0);

    for (let i = 0; i < n; i++) {
        let index = Math.floor(arr[i] / exp) % 10;
        count[index]++;
    }

    for (let i = 1; i < 10; i++) {
        count[i] += count[i - 1];
    }

    for (let i = n - 1; i >= 0; i--) {
        let index = Math.floor(arr[i] / exp) % 10;
        output[count[index] - 1] = arr[i];
        count[index]--;
    }

    for (let i = 0; i < n; i++) {
        arr[i] = output[i];
    }
}

function radixSort(arr) {
    let max = getMax(arr);
    for (let exp = 1; Math.floor(max / exp) > 0; exp *= 10) {
        countingSort(arr, exp);
    }
}

let arr = [170, 45, 75, 90, 802, 24, 2, 66];

console.log("Arreglo desordenado:");
console.log(arr.join(" "));

radixSort(arr);

console.log("Arreglo ordenado:");
console.log(arr.join(" "));
