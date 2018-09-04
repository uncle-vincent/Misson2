<template>
  <div>
    <div style="width: 60%; margin: auto">
      <div style="height: 25px">
        <label class="label">From date: </label>
        <input class="input" v-model="from_date" type="date">
        <label class="label">To date: </label>
        <input class="input" v-model="to_date"  type="date">
        <!--<button class="button is-success" v-on:click="getData(from_date, to_date)">Search Data</button>-->
        <button class="button is-success" v-on:click="getPeriodMarket(from_date, to_date)">Search Market</button>
      </div>
      <div v-if=" showd">
      <div v-for="each_data in marketData" v-bind:key="each_data.id">
        <ul>
          <li>
            date is {{each_data.date}}
          </li>
          <li>
            open price is {{each_data.open_price}}
          </li>
        </ul>
      </div>
      <div>{{result.categoryData}}</div>
      <div>{{marketData.length}}</div>
    </div>
      <div title="k线图" style="position: relative;overflow: hidden;width: 100%;height: 400px;border: 1px solid #E0E0E0;margin: auto"
         id="kline_1" class="" v-if="showk"></div>
    </div>
    <div style="width: 60%; margin: auto">
      <div style="height: 25px">
        <label class="label">date: </label>
        <input class="input" v-model="tradeDate" type="date">
        <label class="label">Org: </label>
        <!--<select v-model="tradeOrg" multiple>
          <option v-for="(org, orgIndex) in tradeOrgOption"
                  v-bind:key="orgIndex" v-bind:value="org.value">
            {{org.text}}
          </option>
        </select>-->
        <select v-model="tradeType" v-on:change="optionSelect()">
          <option v-for="(trade, tradeIndex) in tradeSelectOption"
                  v-bind:value="trade.type.value"  v-bind:key="tradeIndex">
            {{trade.type.text}}
          </option>
        </select>
        <select v-model="tradeBondType">
          <option v-for="(option, optionIndex) in tradeSelection"
                  v-bind:value="option.value" v-bind:key="optionIndex">
            {{option.text}}
          </option>
        </select>
        <button class="button is-success"
                v-on:click="getDateTrade(tradeDate, tradeType)">Search</button>
      </div>
      <div title="bar图" style="position: relative;overflow: hidden;width: 100%;height: 500px;border: 1px solid #E0E0E0;margin: auto"
         id="barline_1" class="" v-if="showk"></div>
    </div>
  </div>
</template>

<script>
import $markets from '../lib/markets'
import $trade from '../lib/trade'
import ECharts from 'vue-echarts/components/ECharts'
// import Datepicker from 'vuejs-datepicker'
import VueDatepickerLocal from 'vue-datepicker-local'
import datepicker from 'vue-date-picker'

export default {
  name: 'MarketSample',
  components: {
    // Datepicker,
    VueDatepickerLocal,
    datepicker,
    'chart': ECharts
  },
  data () {
    return {
      from_date: '',
      to_date: '',
      showk: true,
      showd: false,
      marketData: [],
      result: {},
      tradeResult: {},
      myChart: '',
      marketOption: {},
      tradeOption: {},
      tradeType: 'type',
      tradeBondType: 'treasury_bond',
      tradeOrg: 'Large Commercial Banks/Policy Banks',
      tradeOrgOption: [
        {text: 'Large Commercial Banks/Policy Banks', value: 'Large Commercial Banks/Policy Banks'},
        {text: 'Joint Stock Commercial Banks', value: 'Joint Stock Commercial Banks'},
        {text: 'Foreign institutions', value: 'Foreign institutions'}
      ],
      tradeSelectOption: [
        {
          type: {text: 'By Type', value: 'type'},
          options: [
            {text: 'Treasury Bond', value: 'treasury_bond'},
            {text: 'Policy Financial Bond', value: 'policy_financial_bond'}
          ]
        },
        {
          type: {text: 'By Holding', value: 'holding'},
          options: [
            {text: '1 year', value: 'one_year'},
            {text: '1 to 3 years', value: 'one_to_three_years'}
          ]
        }
      ],
      bondBuyData: [],
      bondSaleData: [],
      bondNetData: [],
      tradeData: {},
      tradeDate: '',
      today: Date.now()
    }
  },
  watch: {
    marketData: function () {
      console.log('in watch')
      this.extractData()
      this.getMarketOption()
      this.myChart = this.$echarts.init(document.getElementById('kline_1'))
      this.myChart.setOption(this.marketOption)
    },
    bondNetData: function () {
      console.log('trade data in watch')
      console.log(this.tradeData)
      this.extractTradeData(this.tradeBondType)
      this.getTradeOption()
      console.log(this.tradeResult)
      this.myTradeChart = this.$echarts.init(document.getElementById('barline_1'))
      this.myTradeChart.setOption(this.tradeOption)
    }
  },
  created () {
    this.getCurrentMarket()
    this.getCurrentTrade(this.tradeType)
  },
  computed: {
    tradeSelection: function () {
      var that = this
      return this.tradeSelectOption.filter(function (item) {
        return item.type.value === that.tradeType
      })[0].options
    }
  },
  methods: {
    extractData: function () {
      var categoryData = []
      var values = []
      for (var i = 0; i < this.marketData.length; i++) {
        var valuesByDay = []
        categoryData.push(this.marketData[i].date)
        valuesByDay.push(this.marketData[i].open_price)
        valuesByDay.push(this.marketData[i].close_price)
        valuesByDay.push(this.marketData[i].low_price)
        valuesByDay.push(this.marketData[i].high_price)
        values.push(valuesByDay)
      }
      this.result = {
        categoryData: categoryData,
        values: values
      }
      return {
        categoryData: categoryData,
        values: values
      }
    },
    extractTradeData: function (type) {
      var keys = ['buy', 'sale', 'net']
      var categoryData = []
      var values = []
      for (var i = 0; i < keys.length; i++) {
        if (i === 0) {
          for (var k = 0; k < this.tradeData[keys[i]].length; k++) {
            categoryData.push((this.tradeData[keys[i]][k])['organization_name'])
          }
        }
        var valuesByOpr = []
        for (var j = 0; j < this.tradeData[keys[i]].length; j++) {
          valuesByOpr.push((this.tradeData[keys[i]][j])[type])
        }
        values.push(valuesByOpr)
      }
      this.tradeResult = {
        categoryData: categoryData,
        values: values
      }
      return {
        categoryData: categoryData,
        values: values
      }
    },
    calulateMA: function (data, dayCount) {
      var result = []
      for (var i = 0, len = data.values.length; i < len; i++) {
        if (i < dayCount) {
          result.push('-')
          continue
        }
        var sum = 0
        for (var j = 0; j < dayCount; j++) {
          sum += data.values[i - j][1]
        }
        result.push(+(sum / dayCount).toFixed(3))
      }
      return result
    },
    getMarket: function (type) {
      this.showk = true
      this.showd = false

      this.extractData(type)

      this.getMarketOption()
      this.myChart.setOption(this.marketOption)
    },
    getPeriodMarket: function (fromDate, toDate) {
      this.from_date = fromDate
      this.to_date = toDate
      $markets.getTreasuryBondFutureMarketByTenYears({
        'from_date': fromDate, 'to_date': toDate}, res => {
        this.marketData = res
      })
    },
    getCurrentMarket: function () {
      $markets.getTreasuryBondFutureMarketByTenYearsCurrent({}, res => {
        this.marketData = res
      })
    },
    getData: function () {
      this.showd = true
      this.showk = false
      $markets.getTreasuryBondFutureMarketByTenYears({
        'from_date': this.from_date, 'to_date': this.to_date}, res => {
        this.marketData = res
      })
    },
    getMarketOption: function () {
      var option = {
        title: {
          text: 'Treasury Bond Future Market By TenYears',
          left: 0
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'line'
          }
        },
        legend: {
          right: '5%',
          data: ['K-Line', 'MA5', 'MA10', 'MA20', 'MA30']
        },
        grid: {
          left: '10%',
          right: '10%',
          bottom: '15%'
        },
        xAxis: {
          type: 'category',
          data: this.result.categoryData.slice(30),
          scale: true,
          boundaryGap: false,
          axisLine: {onZero: false},
          splitLine: {show: false},
          splitNumber: 20,
          min: 'dataMin',
          max: 'dataMax'
        },
        yAxis: {
          scale: true,
          splitArea: {
            show: true
          }
        },
        dataZoom: [
          {
            type: 'inside',
            start: 50,
            end: 100
          },
          {
            show: true,
            type: 'slider',
            y: '90%',
            start: 50,
            end: 100
          }
        ],
        series: [
          {
            name: 'K-Line',
            type: 'candlestick',
            data: this.result.values.slice(30),
            markPoint: {
              label: {
                normal: {
                  formatter: function (param) {
                    return param != null
                      ? Math.round(param.value) : ''
                  }
                }
              },
              data: [
                {
                  name: 'highest value',
                  type: 'max',
                  valueDim: 'highest'
                },
                {
                  name: 'lowest value',
                  type: 'min',
                  valueDim: 'lowest'
                },
                {
                  name: 'average value on close',
                  type: 'average',
                  valueDim: 'close'
                }
              ],
              tooltip: {
                fomatter: function (param) {
                  return param.name + '<br>' +
                    (param.data.coord || '')
                }
              }
            },
            markLine: {
              symbol: ['none', 'none'],
              data: [
                {
                  name: 'min line on close',
                  type: 'min',
                  valueDim: 'close'
                },
                {
                  name: 'max line on close',
                  type: 'max',
                  valueDim: 'close'
                }
              ]
            }
          },
          {
            name: 'MA5',
            type: 'line',
            data: this.calulateMA(this.result, 5).slice(30),
            smooth: true,
            lineStyle: {
              normal: {opacity: 0.5}
            }
          },
          {
            name: 'MA10',
            type: 'line',
            data: this.calulateMA(this.result, 10).slice(30),
            smooth: true,
            lineStyle: {
              normal: {opacity: 0.5}
            }
          },
          {
            name: 'MA20',
            type: 'line',
            data: this.calulateMA(this.result, 20).slice(30),
            smooth: true,
            lineStyle: {
              normal: {opacity: 0.5}
            }
          },
          {
            name: 'MA30',
            type: 'line',
            data: this.calulateMA(this.result, 30).slice(30),
            smooth: true,
            lineStyle: {
              normal: {opacity: 0.5}
            }
          }
        ]
      }
      this.marketOption = option
      return option
    },
    getTradeOption: function () {
      var option = {
        title: {
          text: 'Trade By Organization',
          left: 0
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          right: '5%',
          data: ['Sale', 'Buy', 'Net']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'value'
          }
        ],
        yAxis: [
          {
            type: 'category',
            axisTick: {show: false},
            data: this.tradeResult.categoryData.reverse()
          }
        ],
        series: [
          {
            name: 'Net',
            type: 'bar',
            label: {
              normal: {
                show: true,
                position: 'inside'
              }
            },
            data: this.tradeResult.values[2].reverse()
          },
          {
            name: 'Buy',
            type: 'bar',
            stack: 'Total',
            label: {
              normal: {
                show: true
              }
            },
            data: this.tradeResult.values[0].reverse()
          },
          {
            name: 'Sale',
            type: 'bar',
            stack: 'Total',
            label: {
              normal: {
                show: true,
                position: 'inside'
              }
            },
            data: this.tradeResult.values[1].reverse()
          }
        ]
      }
      this.tradeOption = option
      return option
    },
    getCurrentTrade: function (type) {
      if (type === 'type') {
        $trade.getBondBuyTransactionByTypeCurrent({}, res => {
          this.bondBuyData = res
          this.tradeData['buy'] = res
          $trade.getBondSaleTransactionByTypeCurrent({}, res => {
            this.bondSaleData = res
            this.tradeData['sale'] = res
            $trade.getBondNetTransactionByTypeCurrent({}, res => {
              this.bondNetData = res
              this.tradeData['net'] = res
            })
          })
        })
      } else if (type === 'holding') {
        $trade.getBondBuyTransactionByHoldingCurrent({}, res => {
          this.bondBuyData = res
          this.tradeData['buy'] = res
          $trade.getBondSaleTransactionByHoldingCurrent({}, res => {
            this.bondSaleData = res
            this.tradeData['sale'] = res
            $trade.getBondNetTransactionByHoldingCurrent({}, res => {
              this.bondNetData = res
              this.tradeData['net'] = res
            })
          })
        })
      }
    },
    getDateTrade: function (date, type) {
      console.log(type)
      if (type === 'type') {
        $trade.getBondBuyTransactionByTypeDate({'date': date}, res => {
          this.bondBuyData = res
          this.tradeData['buy'] = res
          $trade.getBondSaleTransactionByTypeDate({'date': date}, res => {
            this.bondSaleData = res
            this.tradeData['sale'] = res
            $trade.getBondNetTransactionByTypeDate({'date': date}, res => {
              this.bondNetData = res
              this.tradeData['net'] = res
            })
          })
        })
      } else if (type === 'holding') {
        $trade.getBondBuyTransactionByHoldingDate({'date': date}, res => {
          this.bondBuyData = res
          this.tradeData['buy'] = res
          $trade.getBondSaleTransactionByHoldingDate({'date': date}, res => {
            this.bondSaleData = res
            this.tradeData['sale'] = res
            $trade.getBondNetTransactionByHoldingDate({'date': date}, res => {
              this.bondNetData = res
              this.tradeData['net'] = res
            })
          })
        })
      }
    },
    optionSelect: function () {
      let that = this
      this.tradeBondType = this.tradeSelectOption.filter(function (item) {
        return item.type.value === that.tradeType
      })[0].options[0].value
    }
  }
}
</script>

<style scoped>

</style>
