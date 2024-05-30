<script lang="ts">
    import {onMount} from "svelte";

    export let fetchTrigger;
    let mean_tails: Record<string, number>;
    let mean_heads: Record<string, number>;
    export let analysis: number = 8;

    let analysis_data: { mean_tails: Record<string, number>, mean_heads: Record<string, number> };

    function fetchData() {
        fetch(`/throws/${analysis}`, {
            method: 'GET',
        })
            .then(response => response.json())
            .then(data => {
                analysis_data = data;
                if (analysis_data) {
                    mean_tails = analysis_data.mean_tails;
                    mean_heads = analysis_data.mean_heads;
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            })
    }

    $: if ($fetchTrigger) fetchData();

    onMount(fetchData)
</script>


{#if analysis_data}
    <section class="mb-20 flex items-center justify-center">
        <div class="w-3/4 flex h-[60vh] justify-center items-center gap-5">
            <div class="w-1/2 h-full gap-5 flex flex-col justify-around items-center">
                <div class="w-full flex h-full justify-between items-center">
                    <div class="w-fit px-3 flex justify-center items-center"><h1>Wurf Nr. </h1></div>
                    <div class="bg-secondary h-8 overflow-hidden flex justify-center items-center"><p
                            class="px-5 text-center content-center">Kopf</p></div>
                    <div class="bg-primary h-8 overflow-hidden flex justify-center items-center"><p
                            class="px-5 text-center content-center">Zahl</p></div>
                </div>
                {#each Object.keys(mean_heads) as key, index}
                    <div class="w-full flex h-full">
                        <div class="w-fit px-3 flex justify-center items-center"><h1>{index + 1}: </h1></div>
                        <div style="width: {mean_heads[key].toFixed(2)}%;"
                             class="bg-secondary h-full overflow-hidden flex justify-center items-center"><p
                                class="px-5 text-center content-center">{mean_heads[key].toFixed(2)} %</p></div>
                        <div style="width: {100 - mean_heads[key].toFixed(2)}%;"
                             class="bg-primary h-full overflow-hidden flex justify-center items-center"><p
                                class="px-5 text-center content-center">{mean_tails[key].toFixed(2)} %</p></div>
                    </div>
                {/each}
            </div>
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
        </div>
    </section>
{/if}

