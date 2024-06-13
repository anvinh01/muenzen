<script context="module" lang="ts">

    // All data in the backend should be in this type
    export type data_entry = {
        title: string,
        info: string,
        heads: Record<string, number> | number,
        tails: Record<string, number> | number
    };
</script>
<script lang="ts">
    import {onMount} from "svelte";
    import Chart from "./Chart.svelte";

    let svgAnalysis: string = '';

    onMount(async () => {
        // import the SVG for the hero section
        const res = await fetch('public/assets/Stats-Analysis.svg');
        svgAnalysis = await res.text();
    });

    export let analysis: number = 8;

    let analysis_data: {
        total: number;
        count: data_entry;
        consecutive: {
            mean: data_entry,
            std: data_entry,
            percentages: data_entry,
            data: data_entry,
        };
    };

    // This is the list of data, which will be passed to the chart component and displayed as a chart
    let data_list: data_entry[] = []
    function fetchData() {
        fetch(`/throws/${analysis}`, {
            method: 'GET',
        })
            .then(response => response.json())
            .then(data => {
                analysis_data = data;
                console.log(analysis_data);
                data_list = [];

                // push the data to the data_list array, to display your data
                if (analysis_data) {
                    data_list.push(analysis_data.count);
                    data_list.push(analysis_data.consecutive.data);
                    data_list.push(analysis_data.consecutive.mean);
                    data_list.push(analysis_data.consecutive.std);
                }
                console.log(data_list);
                data_list = data_list;
            })
            .catch((error) => {
                console.error('Error:', error);
            })
            .finally(
                fetchTrigger.set(false)
            )
    }

    onMount(fetchData)

    export let fetchTrigger: any = false;
    $: if ($fetchTrigger) fetchData();

</script>


<!-- ===============================[ Display different Analysis section ]========================================= -->
{#if analysis_data && data_list}
    <section class="h-fit w-auto">
        {#each data_list as data}
            <div class="h-min-[50vh] my-28 flex content-center justify-center group desktop:my-0">
                <div class="w-3/4 h-full py-14 flex flex-wrap justify-evenly items-center gap-5 group-even:flex-row-reverse">
                    <div class="flex-1 h-full flex items-center gap prose font-default">
                        <div class="prose font-default">
                            <h3 class="my-3" id="#title">
                                {data.title}
                            </h3>
                            <p>
                                {data.info}
                            </p>
                        </div>
                    </div>
                    <div class="h-full flex-1 flex p justify-center desktop:w-11/12 desktop:h-auto">
                        <div class="w-full p-10 rounded-2xl inner-shadow desktop:p-0
                         desktop:shadow-none desktop:h-[60vh]">
                            <Chart data_title="{data.title}" input_data={data}/>
                        </div>
                    </div>
                </div>
            </div>
        {/each}
    </section>
{/if}
