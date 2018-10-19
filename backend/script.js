const csvtojson = require("csvtojson");
const fs = require("fs-extra");


function keysToLowerCase(json) {

  let keys = Object.keys(json[0]).map(key => key.toLowerCase());

  return json.map(({ Province, Type, Subregion, Name, Tel, Latitude, Longitude }) => ({
    [keys[0]]: Province,
    [keys[1]]: Type,
    [keys[2]]: Subregion,
    [keys[3]]: Name,
    [keys[4]]: Tel,
    [keys[5]]: Latitude,
    [keys[6]]: Longitude
  }));
}


async function main() {
  let json = await csvtojson().fromFile("../curated_data/points/shelters_low_res.csv");
  let save = await fs.writeFile("./functions/assets/shelters_low_res.json",JSON.stringify(keysToLowerCase(json),null,2));
}

main();