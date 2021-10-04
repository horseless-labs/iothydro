const path = require('path')
const envPath = path.resolve(process.cwd(), '.env.local')

console.log({ envPath })

require('dotenv').config({ path: envPath })

const mysql = require('serverless-mysql')

const db = mysql({
	  config: {
		      host: process.env.MYSQL_HOST,
		      database: process.env.MYSQL_DATABASE,
		      user: process.env.MYSQL_USERNAME,
		      password: process.env.MYSQL_PASSWORD,
		      port: process.env.MYSQL_PORT,
		    },
})

async function query(q) {
	  try {
		      const results = await db.query(q)
		      await db.end()
		      return results
		    } catch (e) {
			        throw Error(e.message)
			      }
}

async function migrate() {
	try {
		await query(`
			CREATE TABLE IF NOT EXISTS readings (
				id INTEGER AUTO_INCREMENT PRIMARY KEY,
				timestamp TEXT,
				temperature REAL,
				humidity REAL,
				distance REAL
			)
			`)
		console.log('migration ran successfully')
	} catch (e) {
		console.error('could not run migration, double check credentials')
		process.exit(1)
	}
}

migrate().then(() => process.exit())
