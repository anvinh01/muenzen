
describe('My First Test', () => {
	it('Cypress is running!', () => {
        expect(true).to.equal(true)
    })
	it('Should establish a connection to the server', () => {
		cy.visit('http://localhost:5173/');
		cy.get('h1[id=\'#title\']').should('have.text', 'Münzwurf');
	});

    it('Should display the Task options', () => {
        cy.visit('http://localhost:5173/')
        cy.get('#8').should('have.text', '8-Mal werfen');
        cy.get('#10').should('have.text', '10-Mal werfen');
        cy.get('#20').should('have.text', '20-Mal werfen');
    })

})

describe('complete one Task', () => {
	beforeEach(() => {
		cy.visit('http://localhost:5173/');
	});

	it('Should display the Task options', () => {
		cy.get('#8').should('have.text', '8-Mal werfen');
		cy.get('#10').should('have.text', '10-Mal werfen');
		cy.get('#20').should('have.text', '20-Mal werfen');
	});

	it('Should be able to select a Task', () => {
		cy.get('#8').should('have.text', '8-Mal werfen');
		cy.get('#8').click();
	});
});
