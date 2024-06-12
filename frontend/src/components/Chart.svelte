<script lang="ts">
    import {Bar} from 'svelte-chartjs';
    import type {data_entry} from "./Analysis.svelte";
    import {
        Chart,
        Title,
        Tooltip,
        Legend,
        BarElement,
        CategoryScale,
        LinearScale,
    } from 'chart.js';

    Chart.register(
        Title,
        Tooltip,
        Legend,
        BarElement,
        CategoryScale,
        LinearScale
    );
    type ChartData = {
        labels: string[];
        datasets: {
            label: string;
            data: number[];
            borderWidth: number;
            borderColor: string;
            backgroundColor: string;
        }[];
    };

    // Get the data from the input
    export let input_data: data_entry;
    export let data_title: string;

    // Define the chart data
    let data: ChartData = {
        labels: [],
        datasets: [],
    };

    // Update the chart when the data changes
    $: data = (typeof input_data.heads === "object") ?
        {
            labels: Object.keys(input_data.heads),
            datasets: [
                {
                    label: 'Kopf',
                    data: Object.values(input_data.heads),
                    borderWidth: 2, borderColor: 'rgb(239,123,146)',
                    backgroundColor: 'rgb(243,126,149)'
                },
                {
                    label: 'Zahl',
                    data: Object.values(input_data.tails),
                    borderWidth: 2,
                    borderColor: 'rgb(99,180,235)',
                    backgroundColor: 'rgb(102,184,241)'
                },
            ]
        }
        :
        {
            labels: [" "],
            datasets: [
                {
                    label: 'Kopf',
                    data: [input_data.heads],
                    borderWidth: 2, borderColor: 'rgb(239,123,146)',
                    backgroundColor: 'rgb(243,126,149)'
                },
                {
                    label: 'Zahl',
                    data: [input_data.tails],
                    borderWidth: 2,
                    borderColor: 'rgb(99,180,235)',
                    backgroundColor: 'rgb(102,184,241)'
                },
            ]
        }

</script>

<Bar class="" {data} options={{
    responsive: true,
    maintainAspectRatio: false,
    aspectRatio: 1,
    plugins: {
        title: {
            display: true,
            font: {
                size: 20,
            },
            text: data_title,
        },
        legend: {
            position: 'top',
            labels: {
                font: {
                    size: 16,
                },
                padding: 30,
            },
        },
    },
}}/>




