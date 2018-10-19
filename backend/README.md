# Sheeking Shelter GraphQL API

This GraphQL API makes it possible for other developers and NGOs to access the datasets that were curated by the core contributors. 

Currently this API is only making the `shelters_low_res.csv` dataset available until i am given an indication of what datasets should be made publicly available

The schema definition for the GraphQL API can be found by using [**Apollo Playground**](https://us-central1-sheeking-shelter-8443b.cloudfunctions.net/api/graphql)

![Apollo Playground Home](https://preview.ibb.co/jv4MrL/Screenshot-16.png)
###### Apollo Playground Schema
![Apollo Playground Schema](https://preview.ibb.co/d5peBL/Screenshot-17.png)

### How do i access the GraphQL API in my application?
---
If you are familiar with AJAX then you can consume the API by sending a query to the API via a `POST` method. Here's a quick example in Node.js but you can use any programming language of your choice

###### index.js

```javascript
// I'm using axios for making requests
const axios = require("axios");
const url = "https://us-central1-sheeking-shelter-8443b.cloudfunctions.net/api/graphql"

// This query will return the whole dataset

axios.post(url,{
  query: `
    query {
      shelters {
        province
        name
        tel
      }
    }
  `
});

/*
  Response Data

{
  "data": {
    "shelters": [
      {
        "province": "Eastern Cape",
        "name": "Ikhwezi Women Support Centre",
        "tel": "045-8432110"
      },
      {
        "province": "Eastern Cape",
        "name": "Victory House",
        "tel": "043-7226104"
      },
      ...,
      ...
    ]
  }
}

*/
```

```javascript
// You can query the data using 'province' parameter. province takes an 'Enum Province' 

axios.post(url,{
  query: `
    query {
      shelters(province: western_cape) {
        province
        name
        tel
      }
    }
  `
});

/*
  This query will only respond with all the shelters that are based in the Western Cape

  {
  "data": {
    "shelters": [
      {
        "province": "Western Cape",
        "name": "Ikhwezi Women Support Centre",
        "tel": "045-8432110"
      },
      {
        "province": "Western Cape",
        "name": "Victory House",
        "tel": "043-7226104"
      },
      ...,
      ...
    ]
  }
}

*/
```
## What am i using for the backend?
---
I am making use of `Firebase Cloud Functions` for hosting the GraphQL API and the API is built using the `Apollo Server Express` library