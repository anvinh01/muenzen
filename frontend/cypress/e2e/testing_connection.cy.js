describe('My First Test', () => {
    it('Does not do much!', () => {
        expect(true).to.equal(true)
    })

    it('Should display the Task options', () => {
        cy.visit('http://localhost:5173/')
        cy.get('#8').should('have.text', '8-Mal werfen');
        cy.get('#10').should('have.text', '10-Mal werfen');
        cy.get('#20').should('have.text', '20-Mal werfen');
    })

})
