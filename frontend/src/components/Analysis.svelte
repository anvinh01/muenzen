<script context="module" lang="ts">
    export type head_tails = {
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
        count: head_tails;
        consecutive: {
            mean: head_tails,
            std: head_tails,
            percentages: head_tails,
            data: head_tails,
        };
    };

    let data_list: head_tails[] = []
    function fetchData() {
        fetch(`/throws/${analysis}`, {
            method: 'GET',
        })
            .then(response => response.json())
            .then(data => {
                analysis_data = data;
                console.log(analysis_data);
                data_list = [];

                if (analysis_data) {
                    data_list.push(analysis_data.count);
                    data_list.push(analysis_data.consecutive.mean);
                    data_list.push(analysis_data.consecutive.std);
                    data_list.push(analysis_data.consecutive.data);
                }
                console.log(data_list);
                data_list = data_list;
            })
            .catch((error) => {
                console.error('Error:', error);
            })
    }

    onMount(fetchData)

    export let fetchTrigger: any = false;
    $: if ($fetchTrigger) fetchData();

</script>

<!-- ===============================[ Analysis section ]========================================= -->
<section class="flex items-center justify-center mobile:my-8">
    <div class="w-3/4 flex h-[60vh] justify-center items-center gap-5 mobile:h-auto mobile:flex-col">
        <div class="w-1/2 h-fit mobile:w-full">
            <div class="h-fit">
                <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                {@html svgAnalysis}
            </div>
        </div>
        <div class="w-1/2 h-full flex items-center mobile:w-full">
            <div class="prose font-default mobile:text-center">
                <h1 class="my-3" id="#title">Analyse</h1>
                <p>
                    Wir wollen zusammen herausfinden, wie eine Person den Zufall einschätzen. Kommt zuerst Kopf?
                    Zahl?
                    Wie oft denkst du denn kann ein Ergebnis hintereinander vorkommen?
                    Untersuche mit uns wie wir den Zufall auffassen und wie du einen Münzwurf einschätzt.
                </p>
            </div>
        </div>
    </div>
</section>

<!-- ===============================[ Display different Analysis section ]========================================= -->
{#if analysis_data && data_list}
    <section class="h-fit w-auto">
        {#each data_list as data}
            <div class="h-min-[50vh] my-28 flex content-center justify-center group mobile:my-0">
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
                    <div class="h-full flex-1 flex p justify-center mobile:w-11/12 mobile:h-auto">
                        <div class="w-full p-10 rounded-2xl inner-shadow mobile:p-0
                         mobile:shadow-none mobile:h-[60vh]">
                            <Chart data_title="{data.title}" input_data={data}/>
                        </div>
                    </div>
                </div>
            </div>
        {/each}
    </section>
{/if}
