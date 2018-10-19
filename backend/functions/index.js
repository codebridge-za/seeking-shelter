const functions = require('firebase-functions');
const { ApolloServer, gql } = require("apollo-server-express");
const express = require("express");
const cors = require("cors");

const shelters = require("./assets/shelters_low_res.json");

const typeDefs = gql`
  type Query {
    shelters(province: Province): [Shelter!]!
  }

  type Shelter {
    province: String!
    type: String!
    subregion: String!
    name: String!
    tel: String!
    latitude: String!
    longitude: String!
  }

  enum Province {
    western_cape
    eatern_cape
    gauteng
    free_state
    kwazulu_natal
    limpopo
    mpumalanga
    north_west
    northern_cape
  }
`

const resolvers = {
  Province: {
    western_cape: "Western Cape",
    eatern_cape: "Eastern Cape",
    gauteng: "Gauteng",
    free_state: "Free State",
    kwazulu_natal: "Kwazulu-Natal",
    limpopo: "Limpopo",
    mpumalanga: "Mpumalanga",
    north_west: "North West",
    northern_cape: "Northern Cape"
  },
  Query: {
    shelters(root,{ province }) {
      return province ? shelters.filter(shelter => shelter.province === province) : shelters;
    }
  }
}

const app = express();
const server = new ApolloServer({ typeDefs, resolvers, playground: true, introspection: true });

server.applyMiddleware({ app });

module.exports.api = functions.https.onRequest(app);