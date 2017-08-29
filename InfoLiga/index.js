'use strict';

const express = require('express');
const bodyParser = require('body-parser');
const request = require('request');
const dateformat = require('dateformat');
const app = express();
const port = 3000;
const router = express.Router();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.post('/', (req, res) => {
  let gameDay = req.body.text;
  // check if argument is in range
  if(gameDay != '' && gameDay > 0 && gameDay < 35) {
    getGameDayMatches(gameDay).then((response) => {
      let matchUps = '*Die Spiele für den ' + response[0].Group.GroupName + ' lauten:*\n';
      for(let match of response) {
        // check if game has finished or started
        if(match.MatchResults[1] != undefined) {
          matchUps += '_' + match.Team1.TeamName + '_\t*' + match.MatchResults[1].PointsTeam1 +  '* - *' + match.MatchResults[1].PointsTeam2 + '*\t_' + match.Team2.TeamName + '_\n';
        // if game has not finished or started yet
        } else {
          matchUps += '_' + match.Team1.TeamName + '_ - _' + match.Team2.TeamName + '_ am *' + dateformat(match.MatchDateTime, 'dd.mm.yyyy') +
          '* um *' + dateformat(match.MatchDateTime, 'HH:MM', true) + '* Uhr\n';
        }
      }
      res.send(matchUps);
    });
  // if argument is empty or not in range or not a number, send the current matchday
  } else {
    getGameDayMatches('').then((response) => {
      let matchUps = '*Die Spiele für den ' + response[0].Group.GroupName + ' lauten:*\n';
      for(let match of response) {
        // check if game has finished or started
        if(match.MatchResults[1] != undefined) {
          matchUps += '_' + match.Team1.TeamName + '_\t*' + match.MatchResults[1].PointsTeam1 +  '* - *' + match.MatchResults[1].PointsTeam2 + '*\t_' + match.Team2.TeamName + '_\n';
        // if game has not finished or started yet
        } else {
          matchUps += '_' + match.Team1.TeamName + '_ - _' + match.Team2.TeamName + '_ am *' + dateformat(match.MatchDateTime, 'dd.mm.yyyy') +
          '* um *' + dateformat(match.MatchDateTime, 'HH:MM', true) + '* Uhr\n';
        }
      }
      res.send(matchUps);
    });
  }
});

// get the current gameDay
function getGameDay() {
  return new Promise((resolve, reject) => {
    request('https://www.openligadb.de/api/getcurrentgroup/bl1', (error, response, body) => {
      let foo = JSON.parse(response.body);
      let gameDay = JSON.stringify(foo.GroupOrderID);
      resolve(gameDay);
    });
  });
}

// get the current gameDay matches
function getGameDayMatches(gameDay) {
  if(gameDay != '') {
    return new Promise((resolve, reject) => {
      request('https://www.openligadb.de/api/getmatchdata/bl1/2017/' + gameDay, (error, response, body) => {
      let foo = JSON.parse(response.body);
      resolve(foo);
      });
    });
  } else {
    return new Promise((resolve, reject) => {
      let gameDay;
      getGameDay().then((response) => {
        gameDay = response;
        request('https://www.openligadb.de/api/getmatchdata/bl1/2017/' + gameDay, (error, response, body) => {
        let foo = JSON.parse(response.body);
        resolve(foo);
        });
      });
    });
  }
}

// start the server
app.listen(port, (req, res) => {
  console.info('Started Express server on port ' + port)
});
