/** @type {import('tailwindcss').Config} */
export default {
    content: ['./src/**/*.{html,js,svelte,ts}'],
    theme: {
        colors: {
          "background": "var(--background)",
            "primary": "var(--primary)",
            "neutral": "var(--neutral)",
            "white": "var(--white)",
        },
        extend: {
          fontFamily: {
            default: ["Taviraj", "sans-serif"],
          }
        }
    },
    fontFamily: {

    },
    plugins: [require("@tailwindcss/typography")]
};