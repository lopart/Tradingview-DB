const { Kafka } = require('kafkajs')
const TradingView = require("@mathieuc/tradingview");
const input = require('path/to_your/tradingview_input.json');


let client = new TradingView.Client();


var index_list = [];
let k = 1000;

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['localhost:9092'] // local brocker
})

const producer = kafka.producer()

const run = async () => {

  await producer.connect()
  for (let i in input) {
    let chart = new client.Session.Chart();

    chart.setMarket( input[i].market + ":" + input[i].stock,  {
      timeframe: input[i].timeframe,
      to: Math.round(Date.now() / 1000) - 90000,// Seven days before now
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
        
        if (today === 1651001400) {
          if (index_list.includes(i) === false) {
            index_list.push(i);
          }
          if (index_list.length === input.length) {
            console.log("over");
            k = 30000;
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
