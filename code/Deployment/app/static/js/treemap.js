
// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end

// create chart
var chart = am4core.create("treemapDiv", am4charts.TreeMap);
chart.hiddenState.properties.opacity = 0; // this makes initial fade in effect

chart.data = [{
  name: "",
  children: [
    {
      name: "Neutral",
      value: 18423
    }
  ]
},
{
  name: "Joy",
  children: [
    {
      name: "Approval",
      value: 5928
    },
    {
      name: "Admiration",
      value: 5647
    },
    {
      name: "Gratitude",
      value: 3863
    },
    {
      name: "Amusement",
      value: 3081
    },
    {
        name: "0ptimism",
        value: 2887
    },
    {
        name: "Love",
        value: 2745
    },
    {
        name: "Joy",
        value: 2607
    },
    {
        name: "Caring",
        value: 1988
    },
    {
        name: "Excitement",
        value: 1900
    },
    {
        name: "Desire",
        value: 1248
    },
    {
        name: "Relief",
        value: 452
    },
    {
        name: "Pride",
        value: 452
    }
  ]
},
{
  name: "Anger",
  children: [
    {
      name: "Annoyance",
      value: 4443
    },
    {
      name: "Disapproval",
      value: 3774
    },
    {
      name: "Anger",
      value: 2589
    },
    {
        name: "Disgust",
        value: 1704
    }
  ]
},
{
  name: "Surprise",
  children: [
    {
      name: "Curiosity",
      value: 3267
    },
    {
      name: "Realization",
      value: 2867
    },
    {
      name: "Confusion",
      value: 2471
    },
    {
      name: "Surprise",
      value: 1806
    }
  ]
},
{
  name: "Sadness",
  children: [
    {
      name: "Disappointment",
      value: 2771
    },
    {
      name: "Remorse",
      value: 849
    },
    {
        name: "Embarrassment",
        value: 817
    },    
    {
        name: "Sadness",
        value: 2420
    }
  ]
},
{
    name: "Fear",
    children: [
      {
        name: "Fear",
        value: 1048
      },
      {
        name: "Nervousness",
        value: 598
      }
    ]
  }
];

chart.colors.step = 2;

// define data fields
chart.dataFields.value = "value";
chart.dataFields.name = "name";
chart.dataFields.children = "children";

chart.zoomable = false;
var bgColor = new am4core.InterfaceColorSet().getFor("background");

// level 0 series template
var level0SeriesTemplate = chart.seriesTemplates.create("0");
var level0ColumnTemplate = level0SeriesTemplate.columns.template;

level0ColumnTemplate.column.cornerRadius(10, 10, 10, 10);
level0ColumnTemplate.fillOpacity = 0;
level0ColumnTemplate.strokeWidth = 4;
level0ColumnTemplate.strokeOpacity = 0;

// level 1 series template
var level1SeriesTemplate = chart.seriesTemplates.create("1");
var level1ColumnTemplate = level1SeriesTemplate.columns.template;

level1SeriesTemplate.tooltip.animationDuration = 0;
level1SeriesTemplate.strokeOpacity = 1;

level1ColumnTemplate.column.cornerRadius(10, 10, 10, 10)
level1ColumnTemplate.fillOpacity = 1;
level1ColumnTemplate.strokeWidth = 4;
level1ColumnTemplate.stroke = bgColor;

var bullet1 = level1SeriesTemplate.bullets.push(new am4charts.LabelBullet());
bullet1.locationY = 0.5;
bullet1.locationX = 0.5;
bullet1.label.text = "{name}";
bullet1.label.fill = am4core.color("#ffffff");

chart.maxLevels = 2;