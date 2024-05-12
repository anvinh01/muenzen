describe('Site loads content', () => {
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

describe('Selecting 8 coin tosses and chosing random', () => {
	beforeEach(() => {
		cy.visit('http://localhost:5173/');
	});

	it('Should display the Task options', () => {

		// Click on 8 coin tosses
		cy.get('#8')
			.should('be.exist')
			.and('have.text', '8-Mal werfen');
		cy.get('button').contains('8-Mal werfen').click({ force: true });
		// Add a wait command
		cy.wait(1000);
		cy.get('#click').should('be.exist').should('have.text', 'clicked');
		// Selection and options should show up
		cy.get('#Kopf-selection')
			.should('exist')
			.should('have.text', 'Kopf');
		cy.get('#Zahl-selection')
			.should('exist')
			.should('have.text', 'Zahl');


	});
});
