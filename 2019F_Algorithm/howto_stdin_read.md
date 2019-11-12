### C
```c
char* readline() {
    size_t alloc_length = 1024;
    size_t data_length = 0;
    char* data = malloc(alloc_length);

    while (true) {
        char* cursor = data + data_length;
        char* line = fgets(cursor, alloc_length - data_length, stdin);

        if (!line) { break; }

        data_length += strlen(cursor);

        if (data_length < alloc_length - 1 || data[data_length - 1] == '\n') { break; }

        size_t new_length = alloc_length << 1;
        data = realloc(data, new_length);

        if (!data) { break; }

        alloc_length = new_length;
    }

    if (data[data_length - 1] == '\n') {
        data[data_length - 1] = '\0';
    }

    data = realloc(data, data_length);

    return data;
}

char** split_string(char* str) {
    char** splits = NULL;
    char* token = strtok(str, " ");

    int spaces = 0;

    while (token) {
        splits = realloc(splits, sizeof(char*) * ++spaces);
        if (!splits) {
            return splits;
        }

        splits[spaces - 1] = token;

        token = strtok(NULL, " ");
    }

    return splits;
}

char* ar_count_endptr;
char* ar_count_str = readline();
int ar_count = strtol(ar_count_str, &ar_count_endptr, 10);

if (ar_count_endptr == ar_count_str || *ar_count_endptr != '\0') { exit(EXIT_FAILURE); }

char** ar_temp = split_string(readline());

int ar[ar_count];

for (int ar_itr = 0; ar_itr < ar_count; ar_itr++) {
    char* ar_item_endptr;
    char* ar_item_str = ar_temp[ar_itr];
    int ar_item = strtol(ar_item_str, &ar_item_endptr, 10);

    if (ar_item_endptr == ar_item_str || *ar_item_endptr != '\0') { exit(EXIT_FAILURE); }

    ar[ar_itr] = ar_item;
}
```

### C++
```cpp
int ar_count;
cin >> ar_count;
cin.ignore(numeric_limits<streamsize>::max(), '\n');

string ar_temp_temp;
getline(cin, ar_temp_temp);

vector<string> ar_temp = split_string(ar_temp_temp);

vector<int> ar(ar_count);

for (int ar_itr = 0; ar_itr < ar_count; ar_itr++) {
    int ar_item = stoi(ar_temp[ar_itr]);

    ar[ar_itr] = ar_item;
}
```

### Java
```java
private static final Scanner scanner = new Scanner(System.in);

public static void main(String[] args) throws IOException {
    int arCount = Integer.parseInt(scanner.nextLine().trim());

    int[] ar = new int[arCount];

    String[] arItems = scanner.nextLine().split(" ");

    for (int arItr = 0; arItr < arCount; arItr++) {
        int arItem = Integer.parseInt(arItems[arItr].trim());
        ar[arItr] = arItem;
    }
```

### Python 3
```python
ar_count = int(input())

ar = list(map(int, input().rstrip().split()))
```
