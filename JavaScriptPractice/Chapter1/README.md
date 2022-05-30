# Chapter 1 Setting Up a Development Environment Lecture Note

## Type and execute code

### In browser (Developer console)

- Enter: Execute

- Shift + Enter: Multiline

### In HTML documents

```html
<script>
</script>
```

## Console log (standard output?)

- console.warn(object)
- console.error(object)
- console.assert(expression, object)
- console.trace()
- console.count(label)
- console.dir(object)
- console.group()
- console.time(label)
- console.timeEnd(label)

## Variable time time

- Run below code twice, error was occured.
  - already declared variable!

```javascript
const testValue = 40+12;
console.log(testValue);
```

- we can enclose block of code in a set of braces

```javascript
{
  const testValue = 40+12;
  console.log(testValue);
}
```

## Strict mode

- `JavaScript` ignore minor rule breaking that put developers at disadvantage.

```javascript
// This function adds a list of consecutive numbers
function addRange(start, end) {
  let sum = 0;
  for (let i = start; i < end+1; i++) {
    sum += i;
  }
  return sum;
}

// Add numbers from 10 to 15
let startNumber = 10;
let endNumber = 15;
console.log(addRange(startNumber,endNumber)); // Displays 75

// Now add numbers from 1 to 5
startnumber = 1;
endNumber = 5;
console.log(addRange(startNumber,endNumber)); // Displays 0, but we expect 15
```
