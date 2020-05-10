package serenity.pages;

import net.serenitybdd.core.annotations.findby.By;
import net.serenitybdd.core.annotations.findby.FindBy;
import net.serenitybdd.core.pages.WebElementFacade;
import net.thucydides.core.annotations.DefaultUrl;
import net.thucydides.core.pages.PageObject;

import java.util.List;
import java.util.stream.Collectors;

/**
 * @author joj on 5/10/2020
 **/

@DefaultUrl("https://www.emag.ro/")
public class EmagResultPage extends PageObject {

    @FindBy(name="query")
    private WebElementFacade searchTerms;

    @FindBy(className = "searchbox-submit-button")
    private WebElementFacade lookupButton;

    @FindBy(id="js-filter-6411-collapse")
    private WebElementFacade filterParent;

    public void filter() {
        evaluateJavascript("$('#js-filter-6411-collapse').children[0].children[0].click()");
    }

    public void enter_keywords(String keyword) {
        searchTerms.type(keyword);
    }

    public void lookup_terms() {
        lookupButton.click();
    }

    public List<String> getDefinitions() {
        WebElementFacade definitionList = find(By.className("js-products-container"));
        return definitionList.findElements(By.className("js-product-data")).stream()
                .map( element -> element.getText() )
                .collect(Collectors.toList());
    }
}



