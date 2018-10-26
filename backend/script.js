const csvtojson = require("csvtojson");
const fs = require("fs-extra");
const { mapKeys, split } = require("lodash");

function keysToLowerCase(obj) {
  return obj.map(val => mapKeys(val,(value,key) => key.toLowerCase()));
}

async function saveToFileAsJSON(filename) {
  let json = csvtojson().fromFile(`../curated_data/points/${filename}.csv`);
  return fs.writeFile(`./functions/assets/${filename}.json`,JSON.stringify(keysToLowerCase(await json),null,2))
    .then(() => `${filename} was saved`)
    .catch(() => `${filename} was not saved`)
} 

async function main() {
  let files = await fs.readdir("../curated_data/points");
  files.map(file => split(file,".csv")[0]).map(file => saveToFileAsJSON(file));
}

main();