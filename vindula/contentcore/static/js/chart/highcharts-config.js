/*
	Highcharts, TRADUÇÃO PARA O PORTUGLES

*/

var custom_config = { 
	
	credits: {
    	enabled: false  
    },
	lang: {
		loading: 'Carregando...',
		months: ['Janeiro', 'Feveiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
				'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
		shortMonths: ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Set', 'Out', 'Nov', 'Dez'],
		weekdays: ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sabado'],
		decimalPoint: ',',
		thousandsSep: '.',

		printChart: 'Imprimir Grafico',
		contextButtonTitle: 'Exportar Grafico',
		downloadJPEG: 'Download imagem JPEG',
		downloadPDF: 'Download documento PDF',
		downloadPNG: 'Download image PNG',
		downloadSVG: 'Download imagem vetro SVG'
	},

	// Dados para o graficos

	chart:{
		type: 'bar',
	},
	title: {
        text: 'Respostas'
    },
    subtitle: {
        text: ''
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Quantidades'
        }
    },
    tooltip: {
        headerFormat: '<span style="font-size:10px">{point.key}</span><div>',
        pointFormat: '<span style="padding:0"><b>{point.y}</b></span>',
        footerFormat: '</div>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        },
        bar: {
            dataLabels: {
                enabled: true
            }
        }
    },

};