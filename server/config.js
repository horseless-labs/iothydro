const path = require('path');
const envPath = path.resolve(process.cwd(), '.env.local');

require('dotenv').config({path: envPath});

const env = process.env;

const config = {
    db: {
        host: env.MYSQL_HOST,
        user: env.MYSQL_USERNAME,
        password: env.MYSQL_PASSWORD,
        port: env.MYSQL_PORT,
        database: env.MYSQL_DATABASE,
    }
};

module.exports = config;