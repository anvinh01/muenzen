import {sveltekit} from '@sveltejs/kit/vite';
import {defineConfig} from 'vitest/config';
import svgPlugin from 'vite-plugin-svgr';

export default defineConfig({
	plugins: [sveltekit(), svgPlugin()],
	server: {
		fs: {
			allow: ['..', '../../assets']
		}
	},
    test: {
        include: ['src/**/*.{test,spec}.{js,ts}']
    }
});
