describe('My First Test', () => {
    it('Does not do much!', () => {
        expect(true).to.equal(true)
    })

    it('Should visit the site!', () => {
        cy.visit('http://localhost:5173/')
        cy.get('h1').should('have.text', 'Hello World!')
    })

})

