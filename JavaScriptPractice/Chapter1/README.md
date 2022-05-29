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
