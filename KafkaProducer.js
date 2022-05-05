const { Kafka } = require('kafkajs')
const TradingView = require("@mathieuc/tradingview");
const input = require('/Users/artem_lopatenko/workspace/javascript/tradingview_input.json');


let client = new TradingView.Client();


var index_list = [];
let k = 5000;



// Markets:
// - e.g. 'NYSE:MCD','NASDAQ:AAPL' .json
// Indicators:
// - e.g. Bollinger + RSI, Double Strategy (by ChartArt) v1.1   .json
// - e.g. CM_Ultimate_MA_MTF_V2
// Timeframes:
// - 1D, 5D, 1M etc.
// - time from now (days)


const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['localhost:9092']
})

const producer = kafka.producer()

const run = async () => {

  await producer.connect()
  for (let i in input) {
    let chart = new client.Session.Chart();


    chart.setMarket( input[i].market + ":" + input[i].stock,  {
      timeframe: input[i].timeframe,
      to: Math.round(Date.now() / 1000) - 7200,// Two hours before now
      range: -1,
    });

    let publicFmp = TradingView.searchIndicator(input[i].strategy).then(async (indicator) => {
      indicator[0].source = '-';
      let pineIndicator = await indicator[0].get();
      let study = new chart.Study(pineIndicator);
      study.onUpdate((d) => {

        var today = study.periods[0].$time;
        if (index_list.includes(i) === false) {
          console.log(today);
          console.log(Date.now());
          var t = new Date(study.periods[0].$time * 1000);
          var t1 = t.toUTCString();
          var str1 = `{
            "title": "`+ input[i].stock +`",
            "strategy": "`+ input[i].strategy +`",
            "time": "`+ t1 + `",
            "timeframe": "`+ input[i].timeframe + `"
            }`;
          var info = JSON.parse(str1);
          var metrics = study.periods[0];
          var merged = {info, metrics};
          console.log( merged );        
          producer.send({
             topic: 'test',
              messages: [
              { value: JSON.stringify( merged )},
              ],})
          }
        
        if (Math.round(Date.now() / 1000) - today < 1800) {
          if (index_list.includes(i) === false) {
            index_list.push(i);
          }
          if (index_list.length === input.length) {
            console.log("over");
            k = 1800000 - (Date.now() - today * 1000);
            index_list = [];
            //client.end();
          }
        }


          setTimeout(() => { 
              console.log("updating");
              //if (index_list.includes(i) === false) {
                chart.fetchMore(-1);
              //}      
            },
           k );
        

    });
      })
  }
}
run().catch(console.error)
