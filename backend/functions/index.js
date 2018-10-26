const functions = require('firebase-functions');
const { ApolloServer, gql } = require("apollo-server-express");
const express = require("express");
const cors = require("cors");

const shelters = require("./assets/shelters_low_res.json");
const clinics = require("./assets/clinics.json");

const typeDefs = gql`
  type Query {
    shelters(province: Province): [Shelter!]!
    clinics(province: Province): [Clinics!]!
  }

  type Shelter {
    province: String!
    subregion: String!
    type: String!
    name: String!
    tel: String!
    latitude: String!
    longitude: String!
  }

  type Clinics { 
    province: String!
    type: String!
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
    },
    clinics(root,{ province }) {
      return province ? clinics.filter(clinic => clinic.province === province) : clinics;
    }
  }
}

const app = express();
const server = new ApolloServer({ typeDefs, resolvers, playground: true, introspection: true });

server.applyMiddleware({ app });

module.exports.api = functions.https.onRequest(app);