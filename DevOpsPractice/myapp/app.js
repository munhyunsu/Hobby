const express = require('express');
const app = express();
const port = 3002;

const apiRouter = express.Router();

var counter = 0;

apiRouter.get('/', (req, res) => {
  counter = counter + 1;
  res.json({message: 'Hello, world!'});
});

apiRouter.get('/counter', (req, res) => {
  counter = counter + 1;
  res.json({'counter': `${counter}`});
});

app.use('/myweb/api/v1', apiRouter);

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
