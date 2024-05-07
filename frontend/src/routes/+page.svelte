<script>
    import { onMount } from 'svelte';
    import DefaultButton from '../components/+defaultButton.svelte'; // Adjusted import
    let svgHero = '';
    let svgTask = '';

    onMount(async () => {
        // import the SVG for the hero section
        const res = await fetch('public/assets/Coins-pana 1.svg');
        svgHero = await res.text();

        // import the SVG for the task section
        const res2 = await fetch('public/assets/Browser stats-pana 1.svg');
        svgTask = await res2.text();
    });
</script>



<!-- Hero section -->
<div class="pt-8 flex content-center justify-center">
    <div class="w-2/3 flex h-[80vh]">
        <div class="w-1/2 h-full flex items-center ">
            <div class="prose font-default">
                <h1 class="my-3">Münzwurf</h1>
                <h3 class="my-2">Die Wahrscheinlichkeiten eines Münzwurf</h3>
                <p>
                    Finde mit uns heraus wie die Statistik eines Münzwurfs aussieht und wie wir Menschen diese
                    Wahrscheinlichkeiten einschätzen.
                </p>
                <div class="pt-3 my-6">
                    <a class="btn-outer" href="#scenario">Zum Münzwurf</a>
                </div>
            </div>
        </div>
        <div class="w-1/2">
            <div class="w-1/2">
                <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                {@html svgHero}
            </div>
        </div>
    </div>
</div>
<div class="pt-8 flex content-center justify-center">
    <div class="w-2/3 flex h-[80vh]">
        <div class="w-1/2 h-full flex items-center ">
            <div class="prose font-default">
                <h1 class="my-3">Deine Aufgabe</h1>
                <p>
                    Entscheide wie oft du die Münze werfen willst und wähle zwischen Kopf oder Zahl.
                </p>

                <!-- TODO: Adjust the button to the same size as the other buttons -->
                <div class="pt-3 my-6">
                    <button class="btn-outer" id="8">8-Mal werfen</button>
                    <button class="btn-outer" id="10">10-Mal werfen</button>
                    <button class="btn-outer" id="20">20-Mal werfen</button>
                </div>
            </div>
        </div>

        <!-- TODO: Adjust the height of th SVG to th max height of the sections -->
        <div class="w-1/2">
            <div class="h-full w-full flex content-center justify-center">
                <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                {@html svgTask}
            </div>
        </div>
    </div>
</div>
