'use strict';

const express = require('express');
const bodyParser = require('body-parser');
const request = require('request');
const dateformat = require('dateformat');

const app = express();
const port = 3000;
const router = express.Router(); // eslint-disable-line

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

// get the current gameDay
function getGameDay() {
  return new Promise((resolve, reject) => {
    request('https://www.openligadb.de/api/getcurrentgroup/bl1', (error, response, body) => {
      const foo = JSON.parse(response.body);
      const gameDay = JSON.stringify(foo.GroupOrderID);
      resolve(gameDay);
    });
  });
}

// get the current gameDay matches
function getGameDayMatches(gameDay) {
  return new Promise((resolve, reject) => {
    if (gameDay !== '') {
      const requestText = `https://www.openligadb.de/api/getmatchdata/bl1/2017/${gameDay}`;
      request(requestText, (error, response, body) => {
        const foo = JSON.parse(response.body);
        resolve(foo);
      });
    } else {
      getGameDay()
        .then((response) => {
          request(`https://www.openligadb.de/api/getmatchdata/bl1/2017/${response}`, (error, res, body) => {
            const foo = JSON.parse(res.body);
            resolve(foo);
          });
        });
    }
  });
}

app.post('/command', (req, res) => {
  const gameDay = req.body.text;
  const now = new Date();
  console.log(dateformat(now, 'dd.mm.yyyy, HH:MM:ss.l') + '  Post request: /command  ' + gameDay); // eslint-disable-line
  // check if argument is in range
  if (gameDay !== '' && gameDay > 0 && gameDay < 35) {
    getGameDayMatches(gameDay)
      .then((response) => {
        const matchUpsPreText = `*Die Spiele für den ${response[0].Group.GroupName} lauten:*\n`;
        let matchUpsText = '';
        for (const match of response) {
          // check if game has been finished or started
          if (match.MatchResults[1] !== undefined) {
            matchUpsText += `_${match.Team1.TeamName}_\t*${match.MatchResults[1].PointsTeam1}* - *` +
            `${match.MatchResults[1].PointsTeam2}*\t_${match.Team2.TeamName}_\n`;
          // if game has not been finished or started yet
          } else {
            matchUpsText += `_${match.Team1.TeamName}_ - _${match.Team2.TeamName}_ am *` +
            `${dateformat(match.MatchDateTime, 'dd.mm.yyyy')}* um *` +
            `${dateformat(match.MatchDateTime, 'HH:MM', true)}* Uhr\n`;
          }
        }

        const matchUpsArr = {
          attachments: [
            {
              pretext: matchUpsPreText,
              text: matchUpsText,
              mrkdwn_in: [
                'pretext',
                'text',
              ],
              thumb_url: 'http://spielverlagerung.de/wp-content/uploads/2016/01/2016-01-21_Bundesliga.png',
            },
          ],
        };

        res.send(matchUpsArr);
      });
  // if argument is empty or not in range or not a number, send the current matchday
  } else {
    getGameDayMatches('')
      .then((response) => {
        const matchUpsPreText = `*Die Spiele für den ${response[0].Group.GroupName} lauten:*\n`;
        let matchUpsText = '';
        for (const match of response) {
          // check if game has been finished or started
          if (match.MatchResults[1] !== undefined) {
            matchUpsText += `_${match.Team1.TeamName}_\t*${match.MatchResults[1].PointsTeam1}* - *` +
            `${match.MatchResults[1].PointsTeam2}*\t_${match.Team2.TeamName}_\n`;
          // if game has not been finished or started yet
          } else {
            matchUpsText += `_${match.Team1.TeamName}_ - _${match.Team2.TeamName}_ am *` +
            `${dateformat(match.MatchDateTime, 'dd.mm.yyyy')}* um *` +
            `${dateformat(match.MatchDateTime, 'HH:MM', true)}* Uhr\n`;
          }
        }

        const matchUpsArr = {
          attachments: [
            {
              pretext: matchUpsPreText,
              text: matchUpsText,
              mrkdwn_in: [
                'pretext',
                'text',
              ],
              thumb_url: 'http://spielverlagerung.de/wp-content/uploads/2016/01/2016-01-21_Bundesliga.png',
            },
          ],
        };

        res.send(matchUpsArr);
      });
  }
});

// start the server
app.listen(port, (req, res) => {
  console.info(`Started Express server on port ${port}`); // eslint-disable-line
});
