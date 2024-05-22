#!/usr/bin/node

/**
 * Makes a GET request to the provided url using the request library.
 * The response is then parsed as JSON and returned as a promise.
 * If the request is unsuccessful, the error is rejected.
 *
 * @param   {String} url - site url
 * @returns {Promise}    - promise object that resolves
 *                         with parsed JSON response
 *                         and rejects with the request error.
 */
function makeRequest (url) {
    const request = require('request');
    return new Promise((resolve, reject) => {
      request.get(url, (error, response, body) => {
        /**
         * If error is not null, reject the promise with the error.
         * Otherwise, resolve the promise with the parsed JSON response.
         */
        if (error) reject(error);
        else resolve(JSON.parse(body));
      });
    });
  }
  
  /**
   * Entry point - makes requests to Star Wars API
   * for movie info based movie ID passed as a CLI parameter.
   * Retrieves movie character info then prints their names
   * in order of appearance in the initial response.
   */
  async function main () {
    const args = process.argv;
  
    if (args.length < 3) return;
  
    const movieUrl = 'https://swapi-api.alx-tools.com/api/films/' + args[2];
    const movie = await makeRequest(movieUrl);
  
    if (movie.characters === undefined) return;
    for (const characterUrl of movie.characters) {
      const character = await makeRequest(characterUrl);
      console.log(character.name);
    }
  }
  
  main();
