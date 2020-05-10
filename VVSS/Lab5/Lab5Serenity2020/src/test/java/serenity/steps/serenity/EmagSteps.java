package serenity.steps.serenity;

import net.serenitybdd.core.annotations.findby.By;
import net.serenitybdd.core.annotations.findby.FindBy;
import net.serenitybdd.core.pages.WebElementFacade;
import net.thucydides.core.annotations.DefaultUrl;
import net.thucydides.core.annotations.Step;
import serenity.pages.EmagResultPage;

import java.util.List;
import java.util.stream.Collectors;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.hasItem;


/**
 * @author joj on 5/10/2020
 **/

@DefaultUrl("https://www.emag.ro")
public class EmagSteps {

    EmagResultPage emagResultPage;

    @Step
    public void is_the_home_page() {
        emagResultPage.open();
    }

    @Step
    public void looks_for(String term) {
        enters(term);
        starts_search();
    }

    @Step
    public void enters(String keyword) {
        emagResultPage.enter_keywords(keyword);
    }

    @Step
    public void starts_search() {
        emagResultPage.lookup_terms();
    }


    @Step
    public void should_see_definition(String definition) {
        assertThat(emagResultPage.getDefinitions(), hasItem(containsString(definition)));
    }

    @Step
    public void filter_for() {
        emagResultPage.filter();
    }

    @Step
    public void check_filter_not_applied() {
        emagResultPage.check_filter_not_applied();
    }

    @Step
    public void check_filter_applied() throws InterruptedException {
        emagResultPage.check_filter_applied();
    }
}
