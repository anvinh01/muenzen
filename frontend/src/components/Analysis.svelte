<script context="module" lang="ts">
    export type head_tails = { heads: Record<string, number> | number, tails: Record<string, number> | number };
</script>
<script lang="ts">
    import {onMount} from "svelte";
    import Chart from "./Chart.svelte";


    let mean_tails: Record<string, number>;
    let mean_heads: Record<string, number>;
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

    function fetchData() {
        fetch(`/throws/${analysis}`, {
            method: 'GET',
        })
            .then(response => response.json())
            .then(data => {
                analysis_data = data;
                console.log(analysis_data);
                if (analysis_data) {
                    mean_tails = analysis_data.count.tails;
                    mean_heads = analysis_data.count.heads;
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            })
    }

    onMount(fetchData)

    export let fetchTrigger: any = false;
    $: if ($fetchTrigger) fetchData();

</script>


{#if analysis_data && mean_tails && mean_heads}
    <section class="mb-20 flex items-center justify-center">
            <div class="w-1/2 h-full flex items-center">
                <div class="prose font-default">
                    <h1 class="my-3" id="#title">Analyse</h1>
                    <p>
                        Wir wollen zusammen herausfinden, wie eine Person den Zufall einschätzen. Kommt zuerst Kopf?
                        Zahl?
                        Wie oft denkst du denn kann ein Ergebnis hintereinander vorkommen?
                        Untersuche mit uns wie wir den Zufall auffassen und wie du einen Münzwurf einschätzt.
                    </p>
                </div>
            </div>
    </section>
    <section class="pt-8 h-3/4 flex content-center justify-center my-6">
        <div class="w-3/4 h-full flex-wrap flex justify-center items-center">
            <div class="w-1/3 h-full flex items-center ">
                <div class="prose font-default">
                    <h1 class="my-3" id="#title">Münzwurf</h1>
                    <h3 class="my-2">Die Wahrscheinlichkeiten eines Münzwurf</h3>
                    <p>
                        Finde mit uns heraus wie die Statistik eines Münzwurfs aussieht und wie wir Menschen diese
                        Wahrscheinlichkeiten einschätzen.
                    </p>
                </div>
            </div>
            <div class="h-full w-2/3 flex justify-center ">
                <Chart data_title="Anzahl an Kopf und Zahl" input_data={analysis_data.consecutive.mean}/>
            </div>
        </div>
    </section>

    <section class="pt-8 h-3/4 flex content-center justify-center">
        <div class="w-3/4 h-full flex-wrap flex justify-center items-center">
            <div class="w-1/3 h-full flex items-center ">
                <div class="prose font-default">
                    <h1 class="my-3" id="#title">Münzwurf</h1>
                    <h3 class="my-2">Die Wahrscheinlichkeiten eines Münzwurf</h3>
                    <p>
                        Finde mit uns heraus wie die Statistik eines Münzwurfs aussieht und wie wir Menschen diese
                        Wahrscheinlichkeiten einschätzen.
                    </p>
                </div>
            </div>
            <div class="h-full w-2/3 flex justify-center ">
                <Chart data_title="Anzahl an Kopf und Zahl" input_data={analysis_data.consecutive.mean}/>
            </div>
        </div>
    </section>
{/if}

