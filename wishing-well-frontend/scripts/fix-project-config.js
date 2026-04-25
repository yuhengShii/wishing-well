const fs = require("fs");
const path = require("path");

const configPath = path.join(__dirname, "../dist/project.config.json");
const config = JSON.parse(fs.readFileSync(configPath, "utf-8"));

delete config.srcMiniprogramRoot;
delete config.miniprogramRoot;

fs.writeFileSync(configPath, JSON.stringify(config, null, 2) + "\n");
console.log("Fixed project.config.json: removed srcMiniprogramRoot");
